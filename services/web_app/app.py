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

TELEM_ATTEMPT_GEN = "telem:1"
TELEM_SUCCESS_GEN = "telem:2"
TELEM_FAILURE_GEN = "telem:3"

TELEM_SIGNUPS = "telem:4"
TELEM_LOGINS = "telem:5"
TELEM_LOGOUTS = "telem:6"


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


development = int(os.getenv("DEVELOPMENT", "1"))
assert development in [
    0,
    1,
], f"Error, environment variable DEVELOPMENT not loaded correctly: {development}"

app = Flask(__name__, static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "random_secret_key")

DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/app_data/sample.db")
database_folder = os.path.dirname(DATABASE_PATH)
os.makedirs(database_folder, exist_ok=True) # Create the folder if it DNE

users_table = UsersTable(DATABASE_PATH)


if not development:
    from frontend_link import FrontendLink

    frontend_link = FrontendLink()
elif development:
    import mock

    frontend_link = mock.MagicMock()


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
            frontend_link.redis.incr(TELEM_LOGINS)
            return redirect(url_for("create"))
        else:
            flash("Incorrect password.", "danger")

    return render_template("login_user.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    frontend_link.redis.incr(TELEM_LOGOUTS)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()

        # Check that the username is not already in the database
        ans = users_table.query_specific_user_data(username, "id")
        if ans != []:
            flash("Error: Username is already in use!")
            return render_template("register_user.html")

        if not is_password_strong(request.form.get("password1", "")):
            flash(
                "Error! Password Does not meet complexity requirements. Must be length >8, 1x digit, 1x special char, 1x uppercase, 1x lowercase"
            )
            return render_template("register_user.html")

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
        print("Received data from JS")
        frontend_link.redis.incr(TELEM_ATTEMPT_GEN)
        base64_image_data = data["image_data"]
        image_bytes = base64.b64decode(base64_image_data)

        if development:
            print("Detected Development Environment")
            time.sleep(2)

            # Save the buffer to a file
            with open("test.bin", "wb") as f:
                f.write(image_bytes)

            # increment the generationrs counter
            print("Attempting to increment the counter for total generations")
            generations = int(
                users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            users_table.edit_field_of_user(
                session["username"], "total_generations", generations + 1
            )
            generations_new = int(
                users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            assert generations_new == generations + 1
            print("should have successfully increment the total generations")

            return render_template("create.html")

        else:
            print("Contacting the Backend")
            data = frontend_link.publish_message(image_bytes)
            print("Got Response from the backend")

            # 2️⃣ Wrap in a BytesIO object
            buffer = io.BytesIO(data)
            buffer.seek(0)

            # 3️⃣ Use send_file to let the browser download it

            # increment the generationrs counter
            print("Attempting to increment the counter for total generations")
            generations = int(
                users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            users_table.edit_field_of_user(
                session["username"], "total_generations", generations + 1
            )
            generations_new = int(
                users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            assert generations_new == generations + 1
            print("should have successfully increment the total generations")

            return send_file(
                buffer,
                as_attachment=True,
                download_name="cookie_cutter.stl",
                mimetype="model/stl",
            )

    return render_template("create.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # Get the information from the user from the database
    username = session["username"]

    total_genearations = users_table.query_specific_user_data(
        username, "total_generations"
    )
    tokens_remaining = users_table.query_specific_user_data(username, "tokens")
    date_joined = users_table.query_specific_user_data(username, "date_joined")

    user_data = {}
    user_data["username"] = ("Username", username)
    user_data["total_generations"] = ("Total Files Generated", total_genearations)
    user_data["tokens_remaining"] = ("Tokens Remaining", tokens_remaining)
    user_data["date_joined"] = ("Date Joined", date_joined)

    # clean the date

    return render_template("account.html", user_data=user_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
