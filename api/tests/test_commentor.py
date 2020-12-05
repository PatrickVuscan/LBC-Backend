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


class TestCommentor(TestCase):
    "Test all functionality for commentor object in isolation."

    def test_create_comment(self):
        dbb = MockCommentDB()
        commentor = Commentor(dbb)

        cid = commentor.create_comment(post_id=1, user_id=1, content=MSG)
        assert cid == 0

        comment = commentor.view_comment(comment_id=cid)
        assert comment.content == MSG
        assert comment.post_id == 1
        assert comment.user_id == 1

    def test_view_n_comments(self):
        dbb = MockCommentDB()
        commentor = Commentor(dbb)

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
        commentor = Commentor(dbb)

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
