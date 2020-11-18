"""Business logic for commenting."""


class Comment:
    """Comment datastructure."""

    def __init__(self, comment_id: int, post_id: int, user_id: int, content: str):

        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.content = content


class CommentDB:
    """Interface for comment database."""

    def get_comment(self, comment_id: int) -> Comment:
        raise NotImplementedError

    def post_comment(self, post_id: int, user_id: int, content: str) -> int:
        raise NotImplementedError


class Commentor:
    """A class that manages all business logic for user comments."""

    def __init__(self, comment_db: CommentDB):
        self.comment_db = comment_db

    def create_comment(self, post_id: int, user_id: int, content: str):
        return self.comment_db.post_comment(post_id, user_id, content)

    def view_comment(self, comment_id: int):
        return self.comment_db.get_comment(comment_id)
