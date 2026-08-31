from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from src.controller import auth_controller
from src.utils.db import get_db
from src.dto.auth_schema import UserSchema,UserResponseSchema,UserLoginSchema
auth_router = APIRouter(prefix="/auth")



@auth_router.post("/register",response_model=UserResponseSchema)
def create_user(body:UserSchema,db:Session=Depends(get_db)):
    return auth_controller.register_user(body,db)



@auth_router.post("/login")
def create_user(body:UserLoginSchema,db:Session=Depends(get_db)):
    return auth_controller.login_user(body,db)
   