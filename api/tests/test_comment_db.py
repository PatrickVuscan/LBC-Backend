"""Tests CommentDB object."""
from unittest import TestCase
import pytest
from api.database.comment_db import CommentDB


class TestCommentDB(TestCase):
    """Test all functionality for comment db object."""

    @pytest.fixture(autouse=True)
    def init_comment_db(self):
        self.dbb = CommentDB()

    def test_post_comment(self):

        post_id = 1
        user_id = 1
        content = "Hello, World. This should work."

        cid = self.dbb.post_comment(post_id, user_id, content)
        comment = self.dbb.get_comment(cid)

        assert comment.content == content
        assert comment.post_id == post_id
        assert comment.user_id == user_id

    def test_post_two_different_comment(self):
        post_id = 1
        user_id = 1
        content = "Hello for seconds!"

        cid = self.dbb.post_comment(post_id, user_id, content)
        comment = self.dbb.get_comment(cid)

        assert comment.content == content
        assert comment.post_id == post_id
        assert comment.user_id == user_id

        post_id = 1
        user_id = 2
        content = "Seconds on me!"

        cid = self.dbb.post_comment(post_id, user_id, content)
        comment = self.dbb.get_comment(cid)

        assert comment.content == content
        assert comment.post_id == post_id
        assert comment.user_id == user_id
