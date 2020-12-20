"""Business logic for commenting."""
from api.comment.comment_db_interface import CommentDBInterface
from api.comment.comment_validator_interface import CommentValidatorInterface


class Commentor:
    """A class that manages all business logic for user comments."""

    def __init__(self, comment_db: CommentDBInterface, validator: CommentValidatorInterface):
        self.comment_db = comment_db
        self._validator = validator

    def create_comment(self, post_id: int, user_id: int, content: str):
        """Create a comment"""
        self._validator.validate_user(user_id)
        self._validator.validate_post(post_id)
        return self.comment_db.post_comment(post_id, user_id, content)

    def view_comment(self, comment_id: int):
        """View a comment"""
        return self.comment_db.get_comment(comment_id)

    def view_n_comments(self, post_id: int, n: int, offset=0):
        """Return `n` Comments for Post with id `post_id` from offset `o`."""
        self._validator.validate_post(post_id)
        return self.comment_db.get_n_comments(post_id=post_id, n=n, offset=offset)

    def update_comment(self, comment_id: int, user_id: int, content: str):
        """Update Comment with id `comment_id`."""
        self._validator.validate_user_authorization(user_id, comment_id)
        return self.comment_db.update_comment(comment_id, content)

    def delete_comment(self, comment_id: int, user_id: int):
        """Delete Comment with id `comment_id`."""
        self._validator.validate_user_authorization(user_id, comment_id)
        return self.comment_db.delete_comment(comment_id)
