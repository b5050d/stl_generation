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
    session
    )
import base64
from io import BytesIO
import cv2
import numpy as np
from matplotlib import pyplot as plt
import redis
from database import * # TODO - fix this to only import what I care about
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "random secret key"

DATABASE_PATH = "sample.db"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def force_log_out(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            flash(f"Logged {session["username"]} out", "warning")
            session.pop("username")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login", methods = ["GET", "POST"])
@force_log_out
def login():
    if request.method == "POST":
        print("Got a post request!")
        username = request.form.get("username","").strip()
        
        raw_password = request.form.get("password","").strip()
        print(f"Raw Password: {raw_password}")
        password =  generate_password_hash(raw_password)
        print(password)
        
        expected_password = query_specific_user_in_users_table(db_path=DATABASE_PATH, username=username, field="password_hash")
        print(expected_password)

        if expected_password == []:
            flash("User not found")
            return render_template("login_user.html")
        
        if check_password_hash(expected_password, raw_password):
            session['username'] = username
            flash("Login Successful!", "success")
            return redirect(url_for('create'))
        else:
            flash("Incorrect password.", "danger")

    return render_template("login_user.html")


@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = generate_password_hash(request.form.get("password1", "").strip())#generate_password_hash()
        if not check_password_hash(password,  request.form.get("password2", "").strip()):
            flash("Passwords don't match!")
            return render_template("register_user.html")
        else:
            # TODO - Check that the username is a valid email
            # Check that the user is not already present
            add_user_to_users_table(db_path=DATABASE_PATH, username=username, password_hash=password)
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
        print(type(data))
        print(len(data))
        print(data.keys())

        base64_image_data = data["image_data"]

        image_bytes = base64.b64decode(base64_image_data)

        image_stream  = BytesIO(image_bytes)

        nparr = np.frombuffer(image_bytes, np.uint8)

        print(nparr.shape)

        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        print(type(image))
        print(image.shape)
        # plt.imshow(image)
        # plt.show()

    return render_template("create.html")

@app.route("/metrics", methods=["GET"])
def metrics():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
