"""User router methods."""

from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter
from jose import jwt
from sqlalchemy.orm import sessionmaker, Session


from api.database.db_initialize import ENGINE
from api.schema import authentication_schemas
from api.model.table_models import User
import authentication

ROUTER = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 86400
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """Get the database."""
    session = sessionmaker(ENGINE)
    orm_session = session()
    return orm_session


async def get_current_user(dbb: Session = Depends(get_db), token: str = Depends(OAUTH2_SCHEME)):
    """Get the current user."""
    payload = jwt.decode(token, authentication.SECRET_KEY, algorithms=[authentication.ALGORITHM])
    username: str = payload.get("sub")
    token_data = username
    user = authentication.get_user(dbb, username=token_data)
    return user


# Form into to get username/password is more legit (above), but complicates things for now i'll keep it simple
# and just use request body to send username / pass (below)


@ROUTER.post("/users/login", response_model=authentication_schemas.Token)
async def login_for_access_token(user_login: authentication_schemas.UserLogin, dbb: Session = Depends(get_db)):
    """Generate an access token."""
    user = authentication.authenticate_user(dbb, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@ROUTER.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user."""
    return current_user


@ROUTER.post("/users")
def create_user(user: authentication_schemas.UserCreate, dbb: Session = Depends(get_db)):
    """Create a new user."""
    return authentication.create_user(dbb, user)
