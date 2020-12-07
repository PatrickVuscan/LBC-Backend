"""Tests for Commentor object."""
# pylint: disable-all
import pytest
from typing import Optional
from unittest import TestCase
from api.comment.commentor import Commentor
from api.comment.comment import Comment
from api.comment.comment_db_interface import CommentDBInterface
from api.comment.comment_validator_interface import CommentValidatorInterface

MSG = "The Sky Is Blue"


class MockCommentValidator(CommentValidatorInterface):
    """Mock for testing comment database."""

    def validate_user(self, user_id: int):
        """Placeholder validation."""
        pass

    def validate_post(self, post_id: int):
        """Placeholder validation."""
        pass

    def validate_comment(self, comment_id: int):
        """Placeholder validation."""
        pass

    def validate_user_authorization(self, user_id: int, comment_id: int):
        """Placeholder validation."""
        pass


class MockCommentDB(CommentDBInterface):
    "Mock for testing comment database."

    def __init__(self):
        self.comments = {}
        self.next_cid = 0

    def get_comment(self, comment_id):
        return self.comments[comment_id]

    def post_comment(self, post_id, user_id, content):
        comment = Comment(comment_id=self.next_cid, post_id=post_id, user_id=user_id, content=content)
        self.comments[self.next_cid] = comment
        self.next_cid += 1
        return comment.comment_id

    def get_n_comments(self, post_id: int, n: int, offset=0):
        comments = []
        for i in range(n):
            comments.append(self.get_comment(self.next_cid - (i + 1 + offset)))
        return comments

    def update_comment(self, comment_id: int, content: str):
        self.comments[comment_id].content = content


class TestCommentor(TestCase):
    "Test all functionality for commentor object in isolation."

    def test_create_comment(self):
        dbb = MockCommentDB()
        validator = MockCommentValidator()
        commentor = Commentor(dbb, validator)

        cid = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        assert cid == 0

        comment = commentor.view_comment(comment_id=cid)
        assert comment.content == MSG
        assert comment.post_id == 1
        assert comment.user_id == 1

    def test_view_n_comments(self):
        dbb = MockCommentDB()
        validator = MockCommentValidator()
        commentor = Commentor(dbb, validator)

        cid1 = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        cid2 = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        cid3 = commentor.create_comment(post_id=1, user_id=1, content=MSG)

        comments = commentor.view_n_comments(post_id=1, n=3)

        assert len(comments) == 3
        assert comments[0].comment_id == cid3
        assert comments[1].comment_id == cid2
        assert comments[2].comment_id == cid1

    def test_view_n_comments_starting_at_pos_c(self):
        dbb = MockCommentDB()
        validator = MockCommentValidator()
        commentor = Commentor(dbb, validator)

        cid1 = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        cid2 = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        cid3 = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        commentor.create_comment(post_id=1, user_id=1, content=MSG)
        commentor.create_comment(post_id=1, user_id=1, content=MSG)
        commentor.create_comment(post_id=1, user_id=1, content=MSG)

        comments = commentor.view_n_comments(post_id=1, n=3, offset=3)

        assert len(comments) == 3
        assert comments[0].comment_id == cid3
        assert comments[1].comment_id == cid2
        assert comments[2].comment_id == cid1

    def test_update_comment(self):
        uid = 1
        dbb = MockCommentDB()
        validator = MockCommentValidator()
        commentor = Commentor(dbb, validator)

        NEW_MSG = "NEW CONTENT"
        cid = commentor.create_comment(post_id=1, user_id=uid, content=MSG)

        commentor.update_comment(user_id=uid, comment_id=cid, content=NEW_MSG)

        comment = commentor.view_comment(cid)

        assert comment.content == NEW_MSG
