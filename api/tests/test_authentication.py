from unittest import TestCase
import pytest
from fastapi.testclient import TestClient
from app import app

requests = TestClient(app)


class TestAuthentications(TestCase):
    def test_sign_up(self):

        request_body = {"username": "john117", "password": "john117_pass"}

        res = requests.post("/users", json=request_body)

        assert res.status_code == 200

        response_body = res.json()

        print("/users")
        print(response_body)

    def test_login(self):
        # Create user first - Pytest runs in parallel so you cannot assume test order.
        request_body = {"username": "john117", "password": "john117_pass"}

        res = requests.post("/users", json=request_body)

        # Main test starts here.
        request_body = {"username": "john117", "password": "john117_pass"}

        res = requests.post("/users/login", json=request_body)
        response_body = res.json()
        print("users/login body")
        print(response_body)

        assert response_body["token_type"] == "bearer"

        self.__get_user(response_body["token_type"], response_body["access_token"])

    def __get_user(self, token_type, access_token):
        """
        This Function is ONLY meant to be called inside test_login
        """
        request_header = {"Authorization": f"{token_type} {access_token}"}

        res = requests.get("/users/me", headers=request_header)
        response_body = res.json()

        assert response_body["username"] == "john117"

        print("/users/me body")
        print(response_body)


if __name__ == "__main__":
    a = TestAuthentications()
    a.test_sign_up()
    a.test_login()
