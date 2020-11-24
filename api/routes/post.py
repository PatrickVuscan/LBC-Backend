"""API routes for post model."""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from api.database.db_initialize import ENGINE
from api.model.table_models import UserPosts
from api.schema.schemas import CreatePost, UpdatePost


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
        "comments": post.comments,
    }

    return response_body


@ROUTER.post("/posts")
def create_post(request_body: CreatePost, dbb: Session = Depends(get_db)):
    """Create a post"""
    post_data = {
        "username": request_body.username,
        "topic": request_body.topic,
        "date_time": datetime.now(),
        "post_header": request_body.post_header,
        "post_body": request_body.post_body,
    }

    print(post_data)

    dbb.add(UserPosts(**post_data))
    dbb.commit()

    return post_data


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
