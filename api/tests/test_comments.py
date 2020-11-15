from unittest import TestCase
import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestComments(TestCase):
    def test_read_comment(self):
        pid = 1
        cid = 1
        res = client.get(f"/posts/{pid}/comments/{cid}")

        assert res.status_code == 200

        comment = res.json()


        assert comment["comment_id"]  == cid
        assert comment["post_id"] == pid
        assert comment["content"] is not None
        assert comment["likes"] is not None
        assert comment["created_at"] is not None

    def test_read_comments(self):
        pid = 1
        res = client.get(f"/posts/{pid}/comments")

        assert res.status_code == 200

    def test_create_comment(self):
        pid = 1
        res = client.post(f"/posts/{pid}/comments", json={
            "content": "The Sky is Blue."
        })

        assert res.status_code == 200

        comment = res.json()

        assert comment["content"] == "The Sky is Blue."
        assert comment["likes"] == 0
        assert comment["post_id"] == pid

    def test_update_comment(self):
        pid = 1
        res_c = client.post(f"/posts/{pid}/comments", json={
            "content": "The Sky is Blue."
        })

        res_c = res_c.json()

        res = client.put(f"/posts/{pid}/comments/{res_c['comment_id']}", json={
            "content": "'The Sky is blue'"
        })

        assert res.status_code == 200

        u_comment = res.json()
        assert u_comment["comment_id"] == res_c["comment_id"]
        assert u_comment["content"] == "'The Sky is blue'"



