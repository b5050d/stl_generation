"""
Testing script for the database methods
"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.database_methods import UsersTable, get_timestamp


@pytest.fixture
def users(tmp_path):
    users = UsersTable(tmp_path / "test.db")
    assert users.database_path
    return users


def test_get_timestamp():
    ans = get_timestamp()
    assert type(ans) is str


def test_init(tmp_path):
    with pytest.raises(AssertionError):
        users = UsersTable(tmp_path)
        assert users.database_path

    users = UsersTable(tmp_path / "test.db")
    assert users.database_path


def test_does_database_exist(users):
    assert not users.does_database_exist()

    assert not users.does_users_table_exist()

    assert not users.does_database_exist()


def test_does_users_table_exist(users):
    assert not users.does_users_table_exist()


def test_create_users_table(users):
    assert not users.does_database_exist()
    assert not users.does_users_table_exist()

    users.create_users_table()

    assert users.does_database_exist()
    assert users.does_users_table_exist()


def test_generate_add_query_string(users):
    users.fields = ["id", "one", "two", "three"]
    ans = users.generate_add_query_string()
    assert ans == "INSERT INTO Users (one, two, three) VALUES (?,?,?)"


def test_add_user(users):
    username = "ben"
    password = "123"
    users.add_user(username, password)

    with pytest.raises(Exception):
        users.add_user("ben", "a")


def test_generate_specific_user_query(users):
    with pytest.raises(AssertionError):
        ans = users.generate_specific_user_query("oogooaoaboooga")

    ans = users.generate_specific_user_query("password_hash")
    assert ans == "SELECT password_hash FROM Users WHERE username = ?"


def test_query_specific_user_data(users):
    ans = users.query_specific_user_data("ben", "id")
    assert ans == []

    users.add_user("ben", "123")
    ans = users.query_specific_user_data("ben", "password_hash")
    assert ans == "123"


def test_generate_edit_query(users):
    ans = users.generate_edit_query("username")
    assert ans == "UPDATE Users SET username = ? WHERE id = ?"

    with pytest.raises(AssertionError):
        users.generate_edit_query("id")
    with pytest.raises(AssertionError):
        users.generate_edit_query("asdfasddf")


def test_edit_field_of_user(users):
    with pytest.raises(Exception):
        users.edit_field_of_user("ben", "password_hash", "123")

    users.add_user("ben", "123")
    ans = users.query_specific_user_data("ben", "password_hash")
    assert ans == "123"
    users.edit_field_of_user("ben", "password_hash", "456")
    ans = users.query_specific_user_data("ben", "password_hash")
    assert ans == "456"


def test_delete_user(users):
    users.delete_user("ben")

    ans = users.query_specific_user_data("ben", "id")
    assert ans == []

    users.add_user("ben", "123")
    ans = users.query_specific_user_data("ben", "id")
    assert ans == 1

    users.delete_user("ben")
    ans = users.query_specific_user_data("ben", "id")
    assert ans == []
