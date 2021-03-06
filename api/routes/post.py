"""API routes for post model."""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from api.database.db_initialize import ENGINE
from api.model.table_models import UserPosts
from api.schema.schemas import CreatePost, RequestDeletePost, UpdatePost


ROUTER = APIRouter()


def get_db():
    """Get database"""
    session = sessionmaker(ENGINE)
    orm_session = session()
    return orm_session


@ROUTER.get("/posts")
def get_all_posts(dbb: Session = Depends(get_db)):
    """Get all posts"""
    posts = dbb.query(UserPosts).all()
    return posts


@ROUTER.get("/posts/recent/{cursor}")
def get_ten_recent_posts(cursor: int, dbb: Session = Depends(get_db)):
    """Get the ten most recent posts"""
    if cursor == 0:
        posts = dbb.query(UserPosts).order_by(UserPosts.post_id.desc()).limit(10).all()
    else:
        posts = (
            dbb.query(UserPosts).filter(UserPosts.post_id < cursor).order_by(UserPosts.post_id.desc()).limit(10).all()
        )

    return posts


@ROUTER.get("/posts/user/{username}")
def get_posts_by_user(username: str, dbb: Session = Depends(get_db)):
    """Get the ten most recent posts"""
    posts = dbb.query(UserPosts).filter(UserPosts.username == username).all()
    return posts


@ROUTER.get("/posts/{pid}")
def get_single_post(pid: int, dbb: Session = Depends(get_db)):
    """Get a single post"""
    post = dbb.query(UserPosts).filter(UserPosts.post_id == pid).first()

    response_body = {
        "post_id": pid,
        "username": post.username,
        "anonymous": post.anonymous,
        "date_time": post.date_time,
        "topic": post.topic,
        "post_header": post.post_header,
        "post_body": post.post_body,
    }

    return response_body


@ROUTER.post("/posts")
def create_post(request_body: CreatePost, dbb: Session = Depends(get_db)):
    """Create a post"""
    post_data = {
        "username": request_body.username,
        "topic": request_body.topic,
        "anonymous": request_body.anonymous,
        "date_time": datetime.now(),
        "post_header": request_body.post_header,
        "post_body": request_body.post_body,
    }

    new_post = UserPosts(**post_data)
    dbb.add(new_post)
    dbb.commit()
    dbb.refresh(new_post)

    return new_post.post_id


@ROUTER.patch("/posts/{pid}")
def update_post(pid: int, request_body: UpdatePost, dbb: Session = Depends(get_db)):
    """Update a post"""
    user_post = dbb.query(UserPosts).filter(UserPosts.post_id == pid).first()

    user_post.anonymous = request_body.anonymous
    user_post.topic = request_body.topic
    user_post.post_header = request_body.post_header
    user_post.post_body = request_body.post_body

    dbb.commit()

    return request_body


@ROUTER.delete("/posts/{pid}")
def delete_post(pid: int, delete_request: RequestDeletePost, dbb: Session = Depends(get_db)):
    """Delete a post if authorized."""

    record_obj = dbb.query(UserPosts).filter(UserPosts.post_id == pid).first()

    if record_obj.username == delete_request.username:
        dbb.delete(record_obj)
        dbb.commit()
