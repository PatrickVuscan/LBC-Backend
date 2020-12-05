"""Business logic for commenting."""
from api.comment.comment_db_interface import CommentDBInterface


class Commentor:
    """A class that manages all business logic for user comments."""

    def __init__(self, comment_db: CommentDBInterface):
        self.comment_db = comment_db

    def create_comment(self, post_id: int, user_id: int, content: str):
        """Create a comment"""
        return self.comment_db.post_comment(post_id, user_id, content)

    def view_comment(self, comment_id: int):
        """View a comment"""
        return self.comment_db.get_comment(comment_id)

    def view_n_comments(self, post_id: int, n: int, offset=0):
        """Return `n` Comments for Post with id `post_id` from offset `o`."""
        return self.comment_db.get_n_comments(post_id=post_id, n=n, offset=offset)
