import pytest

from database_2 import UsersTable


@pytest.fixture
def users(tmp_path):
    users = UsersTable(tmp_path / "test.db")
    assert users.database_path
    return users

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
    users.fields = ["one", "two", "three"]
    ans = users.generate_add_query_string()
    assert ans == "INSERT INTO Users (one, two, three) VALUES (?,?,?)"

def test_add_user(users):
    username = "ben"
    password = "123"
    users.add_user(username, password)

