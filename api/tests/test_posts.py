"""Tests for posts."""
# pylint: disable-all
from unittest import TestCase
from fastapi.testclient import TestClient
from api.app import app

requests = TestClient(app)


class TestPosts(TestCase):
    """Test all post routes."""

    def test_create_post(self):

        request_body = {
            "username": "Test1",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header",
            "post_body": "The Sky is Blue.",
        }

        res1 = requests.post("/posts", json=request_body)
        post_id = res1.json()

        res2 = requests.get("/posts")
        posts = res2.json()
        post = posts[-1]
        expected_post_id = post["post_id"]

        assert res1.status_code == 200
        assert res2.status_code == 200

        assert post_id == expected_post_id

    def test_get_all_posts(self):
        request_body1 = {
            "username": "Test2",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header1",
            "post_body": "The Sky is Blue.",
        }

        request_body2 = {
            "username": "Test3",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header2",
            "post_body": "The Sky is Blue.",
        }

        res1 = requests.post("/posts", json=request_body1)
        res2 = requests.post("/posts", json=request_body2)
        post_id1 = res1.json()
        post_id2 = res2.json()

        res = requests.get("/posts")

        assert res.status_code == 200
        posts = res.json()

        assert posts[-1]["post_id"] == post_id2
        assert posts[-2]["post_id"] == post_id1

    def test_get_single_post(self):

        res1 = requests.get("/posts")
        posts = res1.json()
        expected_post = posts[-1]
        post_id = expected_post["post_id"]

        res2 = requests.get(f"/posts/{post_id}")

        assert res1.status_code == 200
        assert res2.status_code == 200
        post = res2.json()

        assert post["post_id"] == expected_post["post_id"]
        assert post["username"] == expected_post["username"]
        assert post["anonymous"] is expected_post["anonymous"]
        assert post["date_time"] is not None
        assert post["topic"] == expected_post["topic"]
        assert post["post_header"] == expected_post["post_header"]
        assert post["post_body"] == expected_post["post_body"]

    def test_update_post(self):
        """To test updating a post we first need to get the post's data then we update
        Currently logic is not inplaced for there to be dynamic fields in request body
        so for now we will need to include the fields anonymous, post_header, post_body, topic
        in request body later will make update post request only accept fields which are changing and
        not all these fields every time, but since we do need fields now first send get request for post to update
        then send a patch request"""

        # Create new post to update so doesn't interfere with old test that specify a specific pid
        # Incase we run the test multiple times

        request_body = {
            "username": "Test_Post_Username_2",
            "anonymous": False,
            "topic": "Test_Post_Topic_2",
            "post_header": "Test_Post_Header_2",
            "post_body": "The Sky is bright.",
        }

        requests.post("/posts", json=request_body)

        pid = 2
        post_with_id_1 = requests.get(f"/posts/{pid}").json()

        request_body = {
            "anonymous": post_with_id_1["anonymous"],
            "post_header": post_with_id_1["post_header"],
            "post_body": "Some New Post Body",
            "topic": "Another new Post Topic",
        }

        res_c = requests.patch(f"/posts/{pid}", json=request_body)
        assert res_c.status_code == 200

        post_with_id_1_again = requests.get(f"/posts/{pid}")
        response_body_from_get = post_with_id_1_again.json()

        assert response_body_from_get["post_header"] == post_with_id_1["post_header"]
        assert response_body_from_get["post_body"] == "Some New Post Body"

    def test_get_10_posts(self):

        request_body1 = {
            "username": "Test3",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header",
            "post_body": "The Sky is Blue.",
        }

        request_body2 = {
            "username": "Test4",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header",
            "post_body": "The Sky is Blue.",
        }

        requests.post("/posts", json=request_body1)
        requests.post("/posts", json=request_body2)

        res = requests.get("/posts/recent/2")
        post = res.json()

        expected = requests.get("/posts/1")
        expected_post = expected.json()

        assert res.status_code == 200
        assert post[0]["username"] == expected_post["username"]

    def test_authorized_delete_post(self):

        res1 = requests.get("/posts")
        posts1 = res1.json()
        post1 = posts1[-1]
        post_id1 = post1["post_id"]

        res = requests.delete(f"/posts/{post_id1}", json={"username": post1["username"]})
        assert res.status_code == 200

        res2 = requests.get("/posts")
        posts2 = res2.json()
        post2 = posts2[-1]
        post_id2 = post2["post_id"]

        assert res1.status_code == 200
        assert res2.status_code == 200

        assert post_id1 > post_id2

    def test_unauthorized_delete_post(self):

        res1 = requests.get("/posts")
        posts1 = res1.json()
        post1 = posts1[-1]
        post_id1 = post1["post_id"]

        res = requests.delete(f"/posts/{post_id1}", json={"username": "fake_username"})
        assert res.status_code == 200

        res2 = requests.get("/posts")
        posts2 = res2.json()
        post2 = posts2[-1]
        post_id2 = post2["post_id"]

        assert res1.status_code == 200
        assert res2.status_code == 200

        assert post_id1 == post_id2


if __name__ == "__main__":
    p = TestPosts()
    p.test_create_post()
    p.test_get_all_posts()
    p.test_get_single_post()
    p.test_update_post()
    p.test_get_10_posts()
    p.test_authorized_delete_post()
    p.test_unauthorized_delete_post()
