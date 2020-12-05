"""Tests for Commentor object."""
# pylint: disable-all
from unittest import TestCase
from api.comment.commentor import Commentor
from api.comment.comment import Comment
from api.comment.comment_db_interface import CommentDBInterface

MSG = "The Sky Is Blue"


class MockCommentDB(CommentDBInterface):
    "Mock for testing comment database."

    def __init__(self):
        pass

    def get_comment(self, comment_id):
        return Comment(comment_id=comment_id, post_id=1, user_id=1, content=MSG)

    def post_comment(self, post_id, user_id, content):
        return 10


class TestCommentor(TestCase):
    "Test all functionality for commentor object in isolation."

    def test_create_comment(self):
        dbb = MockCommentDB()
        commentor = Commentor(dbb)

        cid = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        assert cid == 10

        comment = commentor.view_comment(comment_id=cid)
        assert comment.content == MSG
        assert comment.post_id == 1
        assert comment.user_id == 1
