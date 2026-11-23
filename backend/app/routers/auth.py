from app.schemas import UserUpdateRequest  # à importer en haut


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