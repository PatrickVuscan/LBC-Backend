"""Module contains database logic for comment model."""
from sqlalchemy.orm import sessionmaker
from api.database.db_initialize import ENGINE

from api.model.table_models import Comment as CommentModel
from api.posts.comment_db_interface import CommentDBInterface
from api.posts.comment import Comment


class CommentDB(CommentDBInterface):
    """Implementation for comment model."""

    def __init__(self):
        self.orm = sessionmaker(ENGINE)()

    def post_comment(self, post_id: int, user_id: int, content: str) -> int:
        new_comment = CommentModel(post_id=post_id, user_id=user_id, content=content)

        self.orm.add(new_comment)
        self.orm.commit()
        self.orm.refresh(new_comment)

        return new_comment.comment_id

    def get_comment(self, comment_id) -> Comment:
        db_comment = self.orm.query(CommentModel).filter(CommentModel.comment_id == comment_id).first()

        if db_comment is None:
            raise ValueError(f"No such comment with id {comment_id} in db.")
        return Comment(db_comment.comment_id, db_comment.post_id, db_comment.user_id, db_comment.content)
