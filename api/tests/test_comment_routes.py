"""Tests for Comments"""
# pylint: disable-all
from unittest import TestCase
from fastapi.testclient import TestClient
import pytest

from api.app import app

from api.tests.utils.utils import init_post, init_user

client = TestClient(app)


@pytest.mark.usefixtures("init_post", "init_user")
class TestComments(TestCase):
    """Test all comment routes."""

    def test_create_comment(self):
        pid = self.pid
        uid = self.uid

        res = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})

        assert res.status_code == 200
        cid = res.json()

        res_c = client.get(f"/comments/{cid}")
        assert res_c.status_code == 200
        comment = res_c.json()

        assert comment["post_id"] == pid
        assert comment["user_id"] == uid
        assert comment["comment_id"] == cid
        assert comment["content"] == "The Sky is Blue."

    def test_view_n_comments(self):
        pid = self.pid
        uid = self.uid

        res1 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        res2 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        res3 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})

        cid1 = res1.json()
        cid2 = res2.json()
        cid3 = res3.json()

        res_comments = client.get(f"/posts/{pid}/comments/")
        assert res_comments.status_code == 200

        comments = res_comments.json()
        assert comments[0]["comment_id"] == cid3
        assert comments[1]["comment_id"] == cid2
        assert comments[2]["comment_id"] == cid1

    def test_view_n_comments_with_offset(self):
        pid = self.pid
        uid = self.uid

        res1 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        res2 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        res3 = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})
        client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})

        cid1 = res1.json()
        cid2 = res2.json()
        cid3 = res3.json()

        res_comments = client.get(f"/posts/{pid}/comments/?offset=3")
        assert res_comments.status_code == 200

        comments = res_comments.json()
        assert comments[0]["comment_id"] == cid3
        assert comments[1]["comment_id"] == cid2
        assert comments[2]["comment_id"] == cid1
