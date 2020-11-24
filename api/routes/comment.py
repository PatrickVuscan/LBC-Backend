"""API routes for comment model."""

from fastapi import APIRouter
from fastapi.params import Depends

from api.schema.schemas import CommentInDB, CreateComment
from api.posts.commentor import Commentor
from api.posts.comment_db_interface import CommentDBInterface
from api.database.comment_db import CommentDB


ROUTER = APIRouter()


def get_comment_db():
    """Get the database"""
    dbb = CommentDB()

    try:
        yield dbb
    finally:
        dbb.orm.close()


@ROUTER.get("/comments/{cid}", response_model=CommentInDB)
def read_comment(cid: int, dbb: CommentDBInterface = Depends(get_comment_db)):  # type: ignore
    """Read a comment"""
    commentor = Commentor(dbb)
    return commentor.view_comment(cid)


@ROUTER.post("/posts/{pid}/comments", response_model=int)
def create_comment(pid: int, comment: CreateComment, dbb: CommentDBInterface = Depends(get_comment_db)):  # type: ignore
    """Create a comment"""
    commentor = Commentor(dbb)
    return commentor.create_comment(post_id=pid, user_id=comment.user_id, content=comment.content)
