"""API routes for comment model."""
from typing import List
from datetime import datetime
from fastapi import APIRouter

from api.schema.schemas import CommentInDB, CreateComment, RequestCommentUpdate


router = APIRouter()


@router.get("/posts/{pid}/comments/{cid}", response_model=CommentInDB)
def read_comment(pid: int, cid: int):
    return {"comment_id": cid, "post_id": pid , "content": "hello, world!", "likes": 10, "created_at": datetime.now()}


@router.get("/posts/{pid}/comments", response_model=List[CommentInDB])
def read_comments(pid: int):
    return [{"comment_id": 1, "post_id": pid , "content": "hello, world!", "likes": 10, "created_at": datetime.now()}]


@router.post("/posts/{pid}/comments", response_model=CommentInDB)
def create_comment(pid: int, comment: CreateComment):
    return {"comment_id": 1, "post_id": pid , "content": comment.content, "likes": 0, "created_at": datetime.now()}


@router.put("/posts/{pid}/comments/{cid}", response_model=CommentInDB)
def update_comment(pid: int, cid: int, comment: RequestCommentUpdate):
    return {"comment_id": cid,
            "post_id": pid,
            "content": comment.content if comment.content else "Hello, World",
            "likes": comment.likes if comment.likes else 0,
            "created_at": datetime.now()}
