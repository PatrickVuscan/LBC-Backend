"""API routes for post model."""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from api.database.db_initialize import engine
from api.model.table_models import UserPosts
from api.schema.schemas import CreatePost, UpdatePost


router = APIRouter()

def get_db():
    session = sessionmaker(engine)
    orm_session = session()
    return orm_session


@router.get("/posts/{pid}")
def get_single_post(pid: int, db: Session=Depends(get_db)):

    post = db.query(UserPosts).filter(UserPosts.post_id == pid).first()

    response_body = {'post_id': pid,
                     'username': post.username,
                     'anonymous':post.anonymous,
                     'date_time': post.date_time,
                     'topic': post.topic,
                     'post_header': post.post_header,
                     'post_body': post.post_body,
                     'comments': post.comments}

    return response_body


@router.post("/posts")
def create_post(request_body: CreatePost, db: Session=Depends(get_db)):

    post_data = {'username': request_body.username,
            'topic': request_body.topic,
            'date_time': datetime.now(),
            'post_header': request_body.post_header,
            'post_body': request_body.post_body}

    print(post_data)

    db.add(UserPosts(**post_data))
    db.commit()

    return post_data


@router.patch("/posts/{pid}")
def update_post(pid: int, request_body: UpdatePost, db: Session=Depends(get_db)):

    user_post = db.query(UserPosts).filter(UserPosts.post_id == pid).first()

    user_post.anonymous = request_body.anonymous
    user_post.topic = request_body.topic
    user_post.post_header = request_body.post_header
    user_post.post_body = request_body.post_body

    db.commit()

    return request_body
