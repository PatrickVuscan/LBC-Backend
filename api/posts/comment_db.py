"""Database logic for comment model."""
from api.posts.comment import Comment


class CommentDBInterface:
    """Interface for comment database."""

    def get_comment(self, comment_id: int) -> Comment:
        raise NotImplementedError

    def post_comment(self, post_id: int, user_id: int, content: str) -> int:
        raise NotImplementedError
