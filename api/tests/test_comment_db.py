"""Tests CommentDB object."""
# pylint: disable-all
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

    def test_view_n_comments(self):
        post_id = 1
        user_id = 1
        content1 = "Hello 1"
        content2 = "Hello 2"
        content3 = "Testing comments bruh."

        cid1 = self.dbb.post_comment(post_id, user_id, content1)
        cid2 = self.dbb.post_comment(post_id, user_id, content2)
        cid3 = self.dbb.post_comment(post_id, user_id, content3)

        comments = self.dbb.get_n_comments(post_id, n=3)

        assert len(comments) == 3
        assert comments[0].comment_id == cid3
        assert comments[1].comment_id == cid2
        assert comments[2].comment_id == cid1

    def test_view_n_comments_starting_from_offset(self):
        post_id = 1
        user_id = 1
        content1 = "Hello 1"
        content2 = "Hello 2"
        content3 = "Testing comments bruh."
        content4 = "Testing comments bruh!"
        content5 = "Testing comments bruh!!"
        content6 = "Testing comments bruh!!!"

        cid1 = self.dbb.post_comment(post_id, user_id, content1)
        cid2 = self.dbb.post_comment(post_id, user_id, content2)
        cid3 = self.dbb.post_comment(post_id, user_id, content3)
        self.dbb.post_comment(post_id, user_id, content4)
        self.dbb.post_comment(post_id, user_id, content5)
        self.dbb.post_comment(post_id, user_id, content6)

        comments = self.dbb.get_n_comments(post_id, n=3, offset=3)

        assert len(comments) == 3
        assert comments[0].comment_id == cid3
        assert comments[1].comment_id == cid2
        assert comments[2].comment_id == cid1

    def test_update_comment(self):
        NEW_CONTENT = "NEW CONTENT"
        post_id = 1
        user_id = 1
        content1 = "Hello 1"

        cid1 = self.dbb.post_comment(post_id, user_id, content1)

        self.dbb.update_comment(cid1, NEW_CONTENT)

        comment = self.dbb.get_comment(cid1)

        assert comment.content == NEW_CONTENT
