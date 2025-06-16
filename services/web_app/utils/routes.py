
from functools import wraps
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helper_methods import login_required, force_log_out

from flask import render_template, request, flash, session, redirect, url_for
from werkzeug.security import check_password_hash

def init_routes(app):
    """
    Set up routes for our app
    """
    @app.route("/")
    def index():
        return render_template("home.html")


    @app.route("/login", methods=["GET", "POST"])
    @force_log_out
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            expected_password_hash = app.users_table.query_specific_user_data(
                username, "password_hash"
            )

            if expected_password_hash == []:
                flash("User not found")
                return render_template("login_user.html")

            if check_password_hash(
                expected_password_hash, request.form.get("password", "").strip()
            ):
                session["username"] = username
                flash("Login Successful!", "success")
                app.frontend_link.redis.incr(app.config["TELEM_LOGINS"])
                return redirect(url_for("create"))
            else:
                flash("Incorrect password.", "danger")

        return render_template("login_user.html")


    @app.route("/create")
    def create():
        return render_template("home.html")

