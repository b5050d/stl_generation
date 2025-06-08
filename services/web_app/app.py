"""
Main App Functionality.
"""

from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    send_file,
)
import base64
from database_methods import UsersTable
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import os
import time
import io

development = int(os.getenv("DEVELOPMENT", "1"))
assert development in [
    0,
    1,
], f"Error, environment variable DEVELOPMENT not loaded correctly: {development}"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "random_secret_key")

DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/sample.db")

users_table = UsersTable(DATABASE_PATH)

if not development:
    from frontend_link import FrontendLink

    frontend_link = FrontendLink()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def force_log_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            flash(f"Logged {session['username']} out", "warning")
            session.pop("username")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
@force_log_out
def login():
    if request.method == "POST":
        print("Got a post request!")
        username = request.form.get("username", "").strip()
        expected_password_hash = users_table.query_specific_user_data(
            username, "password_hash"
        )

        if expected_password_hash == []:
            flash("User not found")
            return render_template("login_user.html")

        if check_password_hash(
            expected_password_hash, request.form.get("password", "").strip()
        ):
            print("Correct Password!!!")
            session["username"] = username
            flash("Login Successful!", "success")
            return redirect(url_for("create"))
        else:
            flash("Incorrect password.", "danger")

    return render_template("login_user.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password1 = generate_password_hash(request.form.get("password1", "").strip())
        if not check_password_hash(
            password1, request.form.get("password2", "").strip()
        ):
            flash("Passwords don't match!")
            return render_template("register_user.html")
        else:
            # TODO - Check that the username is a valid email
            # Check that the user is not already present
            users_table.add_user(username, password1)
            print("Added user to the user table!")
            flash("Successfully added user!")
            return render_template("login_user.html")
    return render_template("register_user.html")


@app.route("/create")
@login_required
def create():
    return render_template("create.html")


@app.route("/upload_image", methods=["POST"])
@login_required
def upload_image():
    print("I got an image bro!")

    data = request.get_json()
    if data:
        print("We got data! Oh yeah boi!")

        base64_image_data = data["image_data"]
        image_bytes = base64.b64decode(base64_image_data)

        if development:
            time.sleep(2)

            # Save the buffer to a file
            with open("test.bin", "wb") as f:
                f.write(image_bytes)

        else:
            data = frontend_link.publish_message(image_bytes)

            # 2️⃣ Wrap in a BytesIO object
            buffer = io.BytesIO(data)
            buffer.seek(0)

            # 3️⃣ Use send_file to let the browser download it
            return send_file(
                buffer,
                as_attachment=True,
                download_name="myfile.txt",  # you can customize this
                mimetype="text/plain",  # customize for the actual file type!
            )

    return render_template("create.html")


@app.route("/metrics", methods=["GET"])
def metrics():
    pass


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
