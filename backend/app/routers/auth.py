from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import AgentStatus, Consent, PLAN_QUOTAS, Subscription, User
from app.schemas import (
    ErasureResponse,
    SubscriptionResponse,
    SubscriptionUpdateRequest,
    TokenResponse,
    UserLoginRequest,
    UserProfileResponse,
    UserRegisterRequest,
    UserUpdateRequest,
)
from app.security import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentification & Utilisateurs"])


@router.post("/register", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    normalized_email = payload.email.lower().strip()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cette adresse email.",
        )

    max_apps, max_gens = PLAN_QUOTAS[payload.plan]

    user = User(
        full_name=payload.full_name.strip(),
        email=normalized_email,
        hashed_password=hash_password(payload.password),
        agent_status=AgentStatus.ACTIF,
        is_active=True,
    )
    db.add(user)
    db.flush()

    consent = Consent(
        user_id=user.id,
        law_09_08_accepted=payload.consent.law_09_08_accepted,
        gdpr_accepted=payload.consent.gdpr_accepted,
        ai_processing_accepted=payload.consent.ai_processing_accepted,
        policy_version=settings.CURRENT_POLICY_VERSION,
    )
    subscription = Subscription(
        user_id=user.id,
        plan=payload.plan,
        max_applications=max_apps,
        max_ai_generations=max_gens,
        applications_used=0,
        ai_generations_used=0,
    )

    db.add(consent)
    db.add(subscription)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower().strip()).first()
    if not user or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
        )

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfileResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserProfileResponse)
def update_my_account(
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name.strip()

    if payload.email is not None:
        normalized_email = payload.email.lower().strip()
        if normalized_email != current_user.email:
            exists = db.query(User).filter(User.email == normalized_email).first()
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cette adresse email est déjà utilisée.",
                )
            current_user.email = normalized_email

    if payload.password is not None:
        current_user.hashed_password = hash_password(payload.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/me/subscription", response_model=SubscriptionResponse)
def update_subscription(
    payload: SubscriptionUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = current_user.subscription
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Abonnement introuvable.")

    max_apps, max_gens = PLAN_QUOTAS[payload.plan]
    sub.plan = payload.plan
    sub.max_applications = max_apps
    sub.max_ai_generations = max_gens
    db.commit()
    db.refresh(sub)
    return sub


@router.delete("/me", response_model=ErasureResponse)
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    db.delete(current_user)
    db.commit()
    return ErasureResponse(
        message="Compte et données associées supprimés.",
        deleted_user_id=user_id,
    )