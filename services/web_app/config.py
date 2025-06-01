


import os
from datetime import timedelta
currdir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asdfasddfasdf"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(currdir, "app.db")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # ─── Flask-Mail (Email) ────────────────────────────────────────────────────
    # MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.mailgun.org"
    # MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    # MAIL_USE_TLS = True                       # Use TLS (STARTTLS)
    # MAIL_USE_SSL = False                      # Disable SSL (we’re using TLS above)
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "postmaster@YOUR_DOMAIN"
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or "your-smtp-password"
    # MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or "noreply@yourapp.com"

    # ─── Flask-Security-Too Configuration ──────────────────────────────────────
    # A random salt is used when generating password-reset and confirm tokens.
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "another-random-string"

    # Enable/disable user-registration routes:
    SECURITY_REGISTERABLE = True      # Allow users to create an account via /register
    SECURITY_RECOVERABLE = True       # Enable “Forgot Password?” and password reset emails
    SECURITY_CONFIRMABLE = False       # Require e-mail confirmation upon signup

    # By default, send a confirmation email upon registration:
    SECURITY_SEND_REGISTER_EMAIL = False
    # Where to redirect after a successful login (you can change to “/dashboard” later)
    SECURITY_POST_LOGIN_VIEW = "/create"
    # (Optional) After password reset, send the user to login page:
    SECURITY_POST_RESET_VIEW = "/login"
    # (Optional) After email confirmation, send the user to login page:
    SECURITY_POST_CONFIRM_VIEW = "/login"

    # Session / Cookie Security
    # ───────────────────────────────────────────────────────────────────────────
    # Only send session cookies over HTTPS (set to True in production)
    SESSION_COOKIE_SECURE = True
    # Only send the “remember me” cookie over HTTPS
    REMEMBER_COOKIE_SECURE = True
    # Turn on “strong” session protection (detects IP/user-agent changes)
    SESSION_PROTECTION = "strong"
    # Optional: How long “remember me” cookies remain valid
    REMEMBER_COOKIE_DURATION = timedelta(days=14)



