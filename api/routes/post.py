"""API routes for post model."""
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy.orm import Session
from api.model.table_models import USER_POSTS
from api.schema.schemas import PostInDB


router = APIRouter()

@router.get("/posts/{pid}", response_model=PostInDB)
def view_post(db: Session, pid: int):
    return db.query(USER_POSTS).filter(USER_POSTS.post_id == pid).first()


@router.post("/posts/{pid}", response_model=PostInDB)
def create_post(db: Session, pid: int, username: str, anonymous: bool, date_time: datetime, \
    topic: str, post_header: str, post_body: str):
    user_post = USER_POSTS(post_id=pid, username=username, anonymous=anonymous, \
        date_time=date_time, topic=topic, post_header=post_header, post_body=post_body, comments=[])
    db.add(user_post)
    db.commit()
    db.refresh(user_post)
    return user_post
