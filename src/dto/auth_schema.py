from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    email:str
    password:str

class UserResponseSchema(BaseModel):
    id:int
    name:str
    email:str

class UserLoginSchema(BaseModel):
    email:str
    password:str