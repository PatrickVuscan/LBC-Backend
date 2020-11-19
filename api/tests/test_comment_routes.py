from unittest import TestCase
import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestComments(TestCase):
    """Test all comment routes."""

    def test_create_comment(self):
        pid = 1
        uid = 1
        res = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})

        assert res.status_code == 200
        cid = res.json()

        res_c = client.get(f"/comments/{cid}")
        comment = res_c.json()

        assert comment["post_id"] == pid
        assert comment["user_id"] == uid
        assert comment["comment_id"] == cid
        assert comment["content"] == "The Sky is Blue."
