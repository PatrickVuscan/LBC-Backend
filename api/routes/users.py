from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from api.schema import authentication_schemas
import authentication
from datetime import datetime, timedelta
from api.model.table_models import User
from sqlalchemy.orm import sessionmaker, Session
from api.database.db_initialize import engine
from fastapi import APIRouter

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    Session = sessionmaker(engine)
    orm_session = Session()
    return orm_session


async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, authentication.SECRET_KEY, algorithms=[authentication.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = authentication.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


# @router.post("/users/login", response_model=authentication_schemas.Token)
# async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

# Form into to get username/password is more legit (above), but complicates things for now i'll keep it simple
# and just use request body to send username / pass (below)

@router.post("/users/login", response_model=authentication_schemas.Token)
async def login_for_access_token(user_login:authentication_schemas.UserLogin, db: Session = Depends(get_db)):
    user = authentication.authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users")
def create_user(user: authentication_schemas.UserCreate, db: Session=Depends(get_db)):
    return authentication.create_user(db, user)
