from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title:str
    content:str


class User(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class PostCreate(Post):
    title:str
    content:str
    email: EmailStr
