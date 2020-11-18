"""Data validation through pydantic."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseComment(BaseModel):
    """Base validation for comments."""

    content: str


class CommentInDB(BaseComment):
    """Database validation for comments."""

    comment_id: int
    post_id: int
    likes: int
    created_at: datetime

    class Config:
        "Configuration for pydantic."
        orm_mode = True


class CreateComment(BaseComment):
    """Data validation for when creating a new comment."""


class RequestCommentUpdate(BaseModel):
    """Request validation for updating comments."""

    content: Optional[str] = None
    likes: Optional[int] = None
