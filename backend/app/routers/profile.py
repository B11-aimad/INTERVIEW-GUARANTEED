from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CandidateProfile, User
from app.schemas import (
    CandidateProfileResponse,
    CandidateProfileUpdateRequest,
    CandidateProfileValidateRequest,
    ProfileDeleteResponse,
)
from app.security import get_current_user

router = APIRouter(prefix="/profile", tags=["Profil Candidat"])


def _get_or_create_profile(user: User, db: Session) -> CandidateProfile:
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
    if profile is None:
        profile = CandidateProfile(
            user_id=user.id,
            headline="",
            summary="",
            skills=[],
            experiences=[],
            educations=[],
            languages=[],
            preferences={
                "target_role": "",
                "city": "",
                "contract_type": "",
                "remote_allowed": False,
            },
            is_validated=False,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/me", response_model=CandidateProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_or_create_profile(current_user, db)


@router.put("/me", response_model=CandidateProfileResponse)
@router.patch("/me", response_model=CandidateProfileResponse)
def upsert_my_profile(
    payload: CandidateProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(current_user, db)

    if payload.headline is not None:
        profile.headline = payload.headline.strip()
    if payload.summary is not None:
        profile.summary = payload.summary.strip()
    if payload.skills is not None:
        profile.skills = sorted({s.strip() for s in payload.skills if s and s.strip()})
    if payload.experiences is not None:
        profile.experiences = [exp.model_dump() for exp in payload.experiences]
    if payload.educations is not None:
        profile.educations = [edu.model_dump() for edu in payload.educations]
    if payload.languages is not None:
        profile.languages = [lang.model_dump() for lang in payload.languages]
    if payload.preferences is not None:
        merged_prefs = dict(profile.preferences or {})
        merged_prefs.update(payload.preferences.model_dump())
        profile.preferences = merged_prefs

    if payload.is_validated is not None:
        profile.is_validated = payload.is_validated
        profile.validated_at = datetime.now(timezone.utc) if payload.is_validated else None
    else:
        # Toute modification du contenu repasse le profil en attente de validation humaine
        profile.is_validated = False
        profile.validated_at = None

    db.commit()
    db.refresh(profile)
    return profile


@router.post("/me/validate", response_model=CandidateProfileResponse)
def validate_my_profile(
    payload: CandidateProfileValidateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_or_create_profile(current_user, db)
    profile.is_validated = payload.is_validated
    profile.validated_at = datetime.now(timezone.utc) if payload.is_validated else None
    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/me", response_model=ProfileDeleteResponse)
def delete_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profil introuvable.")

    db.delete(profile)
    db.commit()
    return ProfileDeleteResponse(message="Profil candidat supprimé.", user_id=current_user.id)