import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helper_methods import is_password_strong, is_valid_email


def test_is_password_strong():
    password = "a"
    assert not is_password_strong(password)

    password = "aaaaaaaaaaaaaaaaa"
    assert not is_password_strong(password)

    password = "AaAaAaAaAaAaAaAaAaAa"
    assert not is_password_strong(password)

    password = "aaaaaaaaaaaaA!"
    assert not is_password_strong(password)

    password = "aaaaaaaaaaaa1!"
    assert not is_password_strong(password)

    password = "aaaaaaaaaaaA1!"
    assert is_password_strong(password)

    password = ""
    assert not is_password_strong(password)


def test_is_valid_email():
    email = "hi"
    assert not is_valid_email(email)

    email = "@hi"
    assert not is_valid_email(email)

    email = "hi@"
    assert not is_valid_email(email)

    email = "hi@asdf"
    assert not is_valid_email(email)

    email = "hullo!@lotr.com"
    assert not is_valid_email(email)

    email = "hullo@lotr.com"
    assert is_valid_email(email)
