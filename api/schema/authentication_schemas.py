
from typing import List, Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserInDB(UserBase):
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
