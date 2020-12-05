"""Database logic for comment model."""
from typing import Optional
from api.comment.comment import Comment


class CommentDBInterface:
    """Interface for comment database."""

    def get_comment(self, comment_id: int) -> Comment:
        """Get a comment"""
        raise NotImplementedError

    def post_comment(self, post_id: int, user_id: int, content: str) -> int:
        """Post a comment"""
        raise NotImplementedError

    def get_n_comments(self, post_id: int, n: int, offset: Optional[int] = 0):
        raise NotImplementedError
