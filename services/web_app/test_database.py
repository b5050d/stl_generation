import pytest
import os
from database import (
    get_timestamp,
    connect_to_db,
    add_user_to_users_table,
    does_users_table_exist,
    create_users_table,
    query_specific_user_in_users_table,
    delete_a_user,
    edit_field_of_user,
)

def test_get_timestamp():
    ans = get_timestamp()
    assert type(ans) is str


def test_connect_to_db(tmp_path):
    fake_path = tmp_path / "test.db"
    connect_to_db(fake_path)

    # Check that the database is created
    assert os.path.exists(tmp_path)


def test_create_users_table(tmp_path):
    fake_path = tmp_path / "test.db"
    create_users_table(fake_path)
    assert does_users_table_exist(fake_path)
    create_users_table(fake_path)
    create_users_table(fake_path)
    assert does_users_table_exist(fake_path)


def test_does_users_table_exist(tmp_path):
    fake_path = tmp_path / "test.db"
    assert not does_users_table_exist(fake_path)
    create_users_table(fake_path)
    assert does_users_table_exist(fake_path)


def test_add_user_to_users_table(tmp_path):
    fake_path = tmp_path / "test.db"
    # Add the user
    add_user_to_users_table(fake_path, "ben", "ben2")

    # Check that the database is created
    assert os.path.exists(tmp_path)

    # Check that the user got added
    ans = query_specific_user_in_users_table(fake_path, "ben")
    assert ans == 1

    add_user_to_users_table(fake_path, "ben", "ben2")
    ans = query_specific_user_in_users_table(fake_path, "ben")
    assert ans == 1


def test_query_specific_user_in_users_table(tmp_path):
    fake_path = tmp_path / "test.db"
    ans = query_specific_user_in_users_table(fake_path, "ben")
    assert len(ans) == 0
    assert ans == []

    add_user_to_users_table(fake_path, "ben", "ben2")
    ans = query_specific_user_in_users_table(fake_path, "ben", "id")
    assert ans == 1
    ans = query_specific_user_in_users_table(fake_path, "ben", "password_hash")
    assert ans == "ben2"


def test_delete_a_user(tmp_path):
    fake_path = tmp_path / "test.db"

    with pytest.raises(Exception):
        delete_a_user(fake_path, 'ben')
    
    add_user_to_users_table(fake_path, "ben", "ben2")
    ans = query_specific_user_in_users_table(fake_path, "ben", "id")
    assert ans == 1

    delete_a_user(fake_path, 'ben')

    ans = query_specific_user_in_users_table(fake_path, "ben", "id")
    assert ans == []


def test_edit_field_of_user(tmp_path):
    fake_path = tmp_path / "test.db"

    add_user_to_users_table(fake_path, "ben", "ben2")

    ans = query_specific_user_in_users_table(fake_path, "ben", "password_hash")
    assert ans == "ben2"

    edit_field_of_user(fake_path, "ben", "password_hash", "ben3")
    ans = query_specific_user_in_users_table(fake_path, "ben", "password_hash")
    assert ans == "ben3"
