from fastapi import APIRouter,Depends,Response,status
from sqlalchemy.orm import Session

from src.controller import auth_controller
from src.utils.db import get_db
from src.dto.auth_schema import UserSchema,UserResponseSchema,UserLoginSchema
auth_router = APIRouter(prefix="/auth",tags=["Authentication"])


@auth_router.post("/register",response_model=UserResponseSchema)
def create_user(body:UserSchema,db:Session=Depends(get_db)):

    return auth_controller.register_user(body,db)



@auth_router.post("/login")
def create_user(body:UserLoginSchema,response:Response,db:Session=Depends(get_db)):
    
    return auth_controller.login_user(body,db,response)

@auth_router.get("/me", response_model=UserResponseSchema)
def get_me(current_user: UserSchema = Depends(auth_controller.get_current_user)):
    return current_user


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    return auth_controller.logout_user(response)
