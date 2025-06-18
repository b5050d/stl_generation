import pytest
import os
import sys
from werkzeug.security import generate_password_hash

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app_factory import AppFactory


@pytest.fixture()
def factory(tmp_path):
    factory = AppFactory()
    db_path = os.path.join(tmp_path, "sample.db")
    factory.create_app(db_path)
    return factory


def test_home_page(factory):
    with factory.app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"<html" in response.data


def test_login_get(factory):
    with factory.app.test_client() as client:
        response = client.get("/login")
        assert response.status_code == 200
        assert b"<html" in response.data


def test_login_post(factory):
    username = "ben"
    password = "123"

    with factory.app.test_client() as client:
        response = client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"User not found" in response.data

        # Now lets add the user
        factory.app.users_table.add_user(username, generate_password_hash(password))

        response = client.post(
            "/login",
            data={"username": username, "password": "poop"},
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Incorrect password." in response.data

        response = client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=False,
        )
        assert response.status_code == 302
        factory.app.frontend_link.redis.incr.assert_called()
        assert "/create" in response.headers["Location"]


def test_logout(factory):
    with factory.app.test_client() as client:
        response = client.post(
            "/logout",
            follow_redirects=False,
        )
        assert response.status_code == 405  # you shouldnt post to logout

        response = client.get("/logout")
        assert response.status_code == 302  # redirect
        factory.app.frontend_link.redis.incr.assert_not_called()

        # Now: simulate a login by setting session
        with client.session_transaction() as sess:
            sess["username"] = "ben"

        response = client.get("/logout")
        assert response.status_code == 302  # redirect
        factory.app.frontend_link.redis.incr.assert_called()
        assert "/login" in response.headers["Location"]


def test_register(factory):
    with factory.app.test_client() as client:
        response = client.get("/register")
        assert response.status_code == 200

        # Submit bad info
        username = ""
        password1 = "aaaaaaaaaaA9!"
        password2 = "aaaaaaaaaaA9!"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_not_called()
        assert response.status_code == 200
        assert b"Must provide valid email" in response.data

        # Submit bad info
        username = "xxxxxxxxxxxx"
        password1 = "aaaaaaaaaaA9!"
        password2 = "aaaaaaaaaaA9!"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_not_called()
        assert response.status_code == 200
        assert b"Must provide valid email" in response.data

        # Submit bad info
        username = "test@example.com"
        password1 = "aaaaaaaaaaA91!"
        password2 = "aaaaaaaaaaA9!"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_not_called()
        assert response.status_code == 200
        assert b"t match!" in response.data
        assert b"Passwords don" in response.data

        # Submit bad info
        username = "test@example.com"
        password1 = "aaa"
        password2 = "aaa"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_not_called()
        assert response.status_code == 200
        assert b"Password does not meet" in response.data

        # Submit bad info - user already exists
        factory.app.users_table.add_user("test2@example.com", "test")
        username = "test2@example.com"
        password1 = "aaaaaaaaaaA9!"
        password2 = "aaaaaaaaaaA9!"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_not_called()
        assert response.status_code == 200
        assert b"already in use!" in response.data

        # Submit good info
        username = "test@example.com"
        password1 = "aaaaaaaaaaA9!"
        password2 = "aaaaaaaaaaA9!"
        response = client.post(
            "/register",
            data={
                "username": username,
                "password1": password1,
                "password2": password2,
            },
            follow_redirects=False,
        )
        factory.app.frontend_link.redis.incr.assert_called()
        assert response.status_code == 200


def test_create(factory):
    with factory.app.test_client() as client:
        # Not logged in
        response = client.get("/create")
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

        with client.session_transaction() as sess:
            sess["username"] = "fake"
        response = client.get("/create")
        assert response.status_code == 200


def test_upload_image(factory):
    with factory.app.test_client() as client:
        # Attempt get request (illegap)
        response = client.get("/upload_image")
        assert response.status_code == 405

        # Not logged in
        response = client.post("/upload_image")
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

        with client.session_transaction() as sess:
            sess["username"] = "fake"
        factory.app.users_table.add_user("fake", "123")

        response = client.post("/upload_image")
        assert response.status_code == 415  # Bad upload

        response = client.post("/upload_image")
        assert response.status_code == 415  # Bad upload


# def test_pass(factory):
#     pass
