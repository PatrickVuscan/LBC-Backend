"""Utility functions for testing backend API."""
# pylint: disable-all
import pytest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


@pytest.fixture(scope="class")
def init_post(request):
    request_body = {
        "username": "Test_Post_Username",
        "anonymous": False,
        "topic": "Test_Post_Topic",
        "post_header": "Test_Post_Header",
        "post_body": "The Sky is Blue.",
    }
    res = client.post("/posts", json=request_body)
    request.cls.pid = res.json()


@pytest.fixture(scope="class")
def init_user(request):
    request_body = {"username": "george", "password": "george_pass"}

    res = client.post("/users", json=request_body)
    res = res.json()

    if res == {"message": "Username already exists"}:

        res = client.post("/users/login", json=request_body)
        res_body = res.json()
        req_header = {"Authorization": f"{res_body['token_type']} {res_body['access_token']}"}
        res = client.get("/users/me", headers=req_header)
        res = res.json()

    request.cls.uid = res["user_id"]


@pytest.fixture(scope="class")
def init_comment(request):
    pid = request.cls.pid
    uid = request.cls.uid
    res = client.post(f"/posts/{pid}/comments", json={"content": "The Sky is Blue.", "user_id": uid})

    request.cls.cid = res.json()
