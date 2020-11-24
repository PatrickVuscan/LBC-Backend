"""Authentication Schemas"""
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Access Token object"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Access Token Data object"""

    username: Optional[str] = None


class UserBase(BaseModel):
    """Access Token UserBase"""

    username: str


class UserInDB(UserBase):
    """Access Token User Hashed Password"""

    hashed_password: str


class UserCreate(UserBase):
    """Access Token User Password"""

    password: str


class UserLogin(BaseModel):
    """Access Token User Login Information"""

    username: str
    password: str
