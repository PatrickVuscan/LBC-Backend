from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.model.table_models import User
from api.schema.authentication_schemas import *


SECRET_KEY = "fce618e71f40c7384a0e6c4721e4638f50c28c19896d1cfe5b3e4f65fc8d53d6"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(db, user):
    new_user = User(username=user.username, password=get_password_hash(user.password))

    find_username = db.query(User).filter(User.username == new_user.username).all()
    if len(find_username) == 0:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        return {"message": "Username already exists"}
