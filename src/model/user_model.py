from sqlalchemy import Column, DateTime,Integer,String, func
from src.utils.db import Base,engine

class User(Base):
    __tablename__ = "users"
    id= Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password_hash=Column(String,nullable=False)
    role=Column(String ,default='user')
    created_at = Column( DateTime(timezone=True), nullable=False, server_default=func.now() )