import re
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Wrapper function to ensure user is logged  in to access
    certain pages
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def force_log_out(f):
    """
    Wrapper function to force the user to log out before
    accessing a specific page
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            flash(f"Logged {session['username']} out", "warning")
            session.pop("username")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def is_password_strong(password):
    """
    Check if the password is strong enough
    """
    if len(password) < 8:
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in password):
        return False
    return True


def is_valid_email(email):
    """
    Check if there is a valid email in the text
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None
