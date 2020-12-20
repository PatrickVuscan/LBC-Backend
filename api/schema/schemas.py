"""Data validation through pydantic."""

from pydantic import BaseModel


class BaseComment(BaseModel):
    """Base validation for comments."""

    content: str


class CommentInDB(BaseComment):
    """Database validation for comments."""

    comment_id: int
    post_id: int
    user_id: int

    class Config:
        "Configuration for pydantic."
        orm_mode = True


class CreateComment(BaseComment):
    """Data validation for when creating a new comment."""

    user_id: int


class RequestCommentUpdate(BaseModel):
    """Request validation for updating comments."""

    user_id: int
    content: str


class RequestDeleteComment(BaseModel):
    """Request body validation for deleting comments."""

    user_id: int


class RequestDeletePost(BaseModel):
    """Request body validation for deleting posts."""

    username: str


class UpdatePost(BaseModel):
    """ Data Validation for updating post """

    topic: str
    anonymous: bool
    post_header: str
    post_body: str


class CreatePost(UpdatePost):
    """ Data validation for creating post """

    username: str
