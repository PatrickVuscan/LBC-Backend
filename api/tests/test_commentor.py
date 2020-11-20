"""Tests for Commentor object."""
from unittest import TestCase
from api.posts.commentor import Commentor
from api.posts.comment import Comment
from api.posts.comment_db_interface import CommentDBInterface


class MockCommentDB(CommentDBInterface):
    "Mock for testing comment database."

    def __init__(self):
        pass

    def get_comment(self, comment_id):
        return Comment(comment_id=comment_id, post_id=1, user_id=1, content="The Sky Is Blue.")

    def post_comment(self, post_id, user_id, content):
        return 10


class TestCommentor(TestCase):
    "Test all functionality for commentor object in isolation."

    def test_create_comment(self):
        dbb = MockCommentDB()
        commentor = Commentor(dbb)

        cid = commentor.create_comment(post_id=1, user_id=1, content="The Sky Is Blue.")
        assert cid == 10

        comment = commentor.view_comment(comment_id=cid)
        assert comment.content == "The Sky Is Blue."
        assert comment.post_id == 1
        assert comment.user_id == 1
