"""Data validation through pydantic."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BaseComment(BaseModel):
    content: str

class CommentInDB(BaseComment):
    comment_id: int
    post_id: int
    likes: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateComment(BaseComment):
    """Data validation for when creating a new comment."""

class RequestCommentUpdate(BaseModel):
    content: Optional[str] = None
    likes: Optional[int] = None
