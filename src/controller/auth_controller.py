from datetime import timedelta
from src.utils.settings import app_settings
from src.dto.auth_schema import UserSchema, UserLoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.user_model import User
from src.utils.auth_utils import get_password_hash, verify_password, create_access_token


def register_user(body: UserSchema, db: Session):
    is_user_exist = db.query(User).filter(User.email == body.email).first()
    if is_user_exist:
        raise HTTPException(
            status_code=400, detail="User already exist with this email."
        )

    pass_hash = get_password_hash(body.password)
    new_user = User(name=body.name, email=body.email, password_hash=pass_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(body: UserLoginSchema, db: Session):
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="user not found")
    is_valid_user = verify_password(body.password, user.password_hash)
    if not is_valid_user:
        raise HTTPException(status_code=400, detail="user creds not matched")
    access_token_expires = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"name": user.name, "email": user.email},
        expires_delta=access_token_expires,
    )
    return {"message": "user logged in ", "token": token}
