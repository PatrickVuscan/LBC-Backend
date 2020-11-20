"""API routes for post model."""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from api.database.db_initialize import engine
from api.model.table_models import USER_POSTS
from api.schema.schemas import PostInDB


router = APIRouter()

def get_db():
    Session = sessionmaker(engine)
    orm_session = Session()
    return orm_session


@router.get("/posts/{pid}", response_model=PostInDB)
def view_post(pid: int, db: Session=Depends(get_db)):
    return db.query(USER_POSTS).filter(USER_POSTS.post_id == pid).first()


@router.post("/posts/{pid}", response_model=PostInDB)
def create_post(pid: int, username: str, anonymous: bool, topic: str, \
    post_header: str, post_body: str, db: Session=Depends(get_db)):
    user_post = USER_POSTS(post_id=pid, username=username, anonymous=anonymous, \
        date_time=datetime.now(), topic=topic, post_header=post_header, post_body=post_body, comments=[])
    db.add(user_post)
    db.commit()
    db.refresh(user_post)
    return user_post


@router.patch("/posts/{pid}", response_model=PostInDB)
def update_post(pid: int, anonymous: bool, topic: str, \
    post_header: str, post_body: str, db: Session=Depends(get_db)):
    user_post = db.query(USER_POSTS).get(post_id=pid)
    user_post.anonymous = anonymous
    user_post.topic = topic
    user_post.post_header = post_header
    user_post.post_body = post_body

    db.commit()
    return user_post
