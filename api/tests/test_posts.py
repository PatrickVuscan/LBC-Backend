from unittest import TestCase
import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestPosts(TestCase):
    def test_read_post(self):
        pid = 1
        res = client.get(f"/posts/{pid}")

        assert res.status_code == 200

        post = res.json()


        assert post["post_id"]  == pid
        assert post["username"] == "test_1_username"
        assert post["anonymous"] is False
        assert post["date_time"] is not None
        assert post["topic"] == "Police"
        assert post["post_header"] == "Police Post Header (test_1)"
        assert post["post_body"] == "Police Post Body (test_1). \n Line 2. \n Line 3."
        assert post["comments"] == []


    def test_create_post(self):
        pid = 1
        res = client.post(f"/posts/{pid}", json={
            "post_body": "Post body updated."
        })

        assert res.status_code == 200

        post = res.json()

        assert post["post_body"] == "The Sky is Blue."
        assert post["post_id"] == pid


    def test_update_comment(self):
        pid = 1
        res_c = client.patch(f"/posts/{pid}", json={
            "post_body": "Post body updated."
        })

        res_c = res_c.json()

        res = client.get(f"/posts/{pid}/']")

        assert res.status_code == 200

        u_post = res.json()
        assert u_post["post_body"] == res_c["post_body"]
        assert u_post["post_id"] == res_c["post_id"]



