from datetime import timedelta
from fastapi import Depends, HTTPException, status,Response
from fastapi.security import OAuth2PasswordBearer
from src.utils.settings import app_settings
from src.dto.auth_schema import UserSchema, UserLoginSchema
from sqlalchemy.orm import Session
from src.model.user_model import User
from src.utils.auth_utils import get_password_hash, verify_password, create_access_token
import jwt
from src.utils.db import get_db
from fastapi import Cookie
COOKIE_NAME = "access_token"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def register_user(body: UserSchema, db: Session):
    is_user_exist = db.query(User).filter(User.email == body.email).first()
    if is_user_exist:
        raise HTTPException(
            status_code=400, detail="User already exist with this email."
        )

    pass_hash = get_password_hash(body.password)
    new_user = User(name=body.name, email=body.email, password_hash=pass_hash,role=body.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(body: UserLoginSchema ,db: Session,response:Response):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # refresh_token_expires = timedelta(days=app_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    # refresh_token = create_access_token(
    #     data={"sub": str(user.id)},
    #     expires_delta=refresh_token_expires,
    # )
    response.set_cookie(
    key=COOKIE_NAME,
    value=access_token,
    httponly=True,
    secure=True,
    samesite="none",
)

    return { "message": "Login successful"}


def get_current_user(
    access_token: str | None = Cookie(default=None), 
    db: Session = Depends(get_db)
): 
    print(access_token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception

    try:

        payload = jwt.decode(
            access_token,
            app_settings.SECRET_KEY,
            algorithms=[app_settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user

def logout_user(response: Response):
    response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=True,    
            samesite="none" 
        )   
    return {"details": "Successfully logged out"}