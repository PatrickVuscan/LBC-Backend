"""Database logic for comment model."""
import abc
from api.comment.comment import Comment


class CommentDBInterface(metaclass=abc.ABCMeta):
    """Interface for comment database."""

    @abc.abstractmethod
    def get_comment(self, comment_id: int) -> Comment:
        """Get a comment"""
        raise NotImplementedError

    @abc.abstractmethod
    def post_comment(self, post_id: int, user_id: int, content: str) -> int:
        """Post a comment"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_n_comments(self, post_id: int, n: int, offset=0):
        """Get `n` comments from db."""
        raise NotImplementedError

    @abc.abstractmethod
    def update_comment(self, comment_id: int, content: str):
        """Update a comment."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete_comment(self, comment_id: int):
        """Delete a comment."""
        raise NotImplementedError
