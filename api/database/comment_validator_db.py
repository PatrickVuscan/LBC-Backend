"""Module contains database validation logic for comment model.""" ""
from sqlalchemy.orm import sessionmaker
from api.database.db_initialize import ENGINE
from api.model.table_models import Comment as CommentModel, User as UserModel, UserPosts as PostModel

from api.comment.comment_validator_interface import CommentValidatorInterface


class CommentValidatorDB(CommentValidatorInterface):
    """Database validation for comment model."""

    def __init__(self):
        self.orm = sessionmaker(ENGINE)()

    def validate_user(self, user_id: int):
        db_user = self.orm.query(UserModel).filter(UserModel.user_id == user_id).first()

        if db_user is None:
            raise ValueError(f"User with id {user_id} does not exist!")

    def validate_post(self, post_id: int):
        db_post = self.orm.query(PostModel).filter(PostModel.post_id == post_id).first()

        if db_post is None:
            raise ValueError(f"Post with id {post_id} does not exist!")

    def validate_comment(self, comment_id: int):
        db_comment = self.orm.query(CommentModel).filter(CommentModel.comment_id == comment_id).first()

        if db_comment is None:
            raise ValueError(f"Comment with id {comment_id} does not exist!")

    def validate_user_authorization(self, user_id: int, comment_id: int):
        self.validate_user(user_id)
        self.validate_comment(comment_id)

        db_comment = self.orm.query(CommentModel).filter(CommentModel.comment_id == comment_id).first()

        if db_comment.user_id != user_id:
            raise PermissionError("Access Denied: You are not allowed to modify this comment.")
