from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    email:str
    password:str
    role: str = "user"

class UserResponseSchema(BaseModel):
    id:int
    name:str
    email:str
    role:str



class UserLoginSchema(BaseModel):
    email:str
    password:str