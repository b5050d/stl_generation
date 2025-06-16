import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import AppFactory
from werkzeug.security import generate_password_hash

@pytest.fixture()
def factory(tmp_path):
    factory = AppFactory()
    db_path = os.path.join(tmp_path, "sample.db")
    app = factory.create_app(db_path)
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

@pytest.mark.skip()
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
        # assert response.status_code == 200
        factory.app.frontend_link.incr.assert_called()
        # assert b"Login Successful!" in response.data