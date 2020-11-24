"""Tests for posts."""
from unittest import TestCase
from fastapi.testclient import TestClient
from app import app

requests = TestClient(app)


class TestPosts(TestCase):
    """Test all post routes."""

    def test_get_all_posts(self):
        res = requests.get("/posts")

        assert res.status_code == 200
        posts = res.json()

        assert len(posts) == 7

    def test_get_single_post(self):

        pid = 1
        res = requests.get(f"/posts/{pid}")

        assert res.status_code == 200
        post = res.json()

        assert post["post_id"] == pid
        assert post["username"] == "Test_Post_Username"
        assert post["anonymous"] is False
        assert post["date_time"] is not None
        assert post["topic"] == "Test_Post_Topic"
        assert post["post_header"] == "Test_Post_Header"
        assert post["post_body"] == "The Sky is Blue."
        assert post["comments"] == ""

        print("Test Get Single Post Passed")

    def test_create_post(self):

        request_body = {
            "username": "Test_Post_Username",
            "anonymous": False,
            "topic": "Test_Post_Topic",
            "post_header": "Test_Post_Header",
            "post_body": "The Sky is Blue.",
        }

        res = requests.post("/posts", json=request_body)
        post = res.json()

        assert res.status_code == 200
        assert post["post_body"] == "The Sky is Blue."

        print("Test Create Post Passed")

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

        print("Test Update Post")


if __name__ == "__main__":
    p = TestPosts()
    # p.test_get_all_posts()
    p.test_create_post()
    p.test_get_single_post()
    p.test_update_post()
