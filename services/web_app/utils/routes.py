from flask import render_template, request, flash, session, redirect, url_for, send_file
from werkzeug.security import check_password_hash, generate_password_hash
import os
import sys
import io
import base64

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helper_methods import (
    login_required,
    force_log_out,
    is_valid_email,
    is_password_strong,
)


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

    @app.route("/logout")
    def logout():
        if "username" in session:
            session.pop("username", None)
            flash("You have been logged out.", "info")
            app.frontend_link.redis.incr(app.config["TELEM_LOGOUTS"])
        else:
            flash("No user was logged in to log out")
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()

            # Is this a valid email?
            if not is_valid_email(username):
                flash("Must provide valid email address!")
                return render_template("register_user.html")

            # Check that the username is not already in the database
            ans = app.users_table.query_specific_user_data(username, "id")
            if ans != []:
                flash("Error: Username is already in use!")
                return render_template("register_user.html")

            # Check that the password is strong enough
            if not is_password_strong(request.form.get("password1", "")):
                flash(
                    "Error! Password does not meet complexity requirements. Must be length >8, 1x digit, 1x special char, 1x uppercase, 1x lowercase"
                )
                return render_template("register_user.html")

            password1 = generate_password_hash(
                request.form.get("password1", "").strip()
            )
            if not check_password_hash(
                password1, request.form.get("password2", "").strip()
            ):
                flash("Passwords don't match!")
                return render_template("register_user.html")
            else:
                app.users_table.add_user(username, password1)
                print("Added user to the user table!")
                flash(
                    "Successfully added user! Please verify your email before you can login"
                )
                app.frontend_link.redis.incr(app.config["TELEM_SIGNUPS"])

                # # Send the email to verify the account
                # verification_token = app.s.dumps(username, salt="email-confirm")
                # link = url_for(
                #     "confirm_email", token=verification_token, _external=True
                # )
                # msg = Message("Confirm Your Email", recipients=[username])
                # msg.body = f"Click the link to confirm your email: {link}"
                # self.mail.send(msg)

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
            app.frontend_link.redis.incr(app.config["TELEM_ATTEMPT_GEN"])
            base64_image_data = data["image_data"]
            image_bytes = base64.b64decode(base64_image_data)

            print("Contacting the Backend")
            data = app.frontend_link.publish_message(image_bytes)
            print("Got Response from the backend")

            # Wrap in a BytesIO object
            buffer = io.BytesIO(data)
            buffer.seek(0)

            # increment the generations counter
            print("Attempting to increment the counter for total generations")
            generations = int(
                app.users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            app.users_table.edit_field_of_user(
                session["username"], "total_generations", generations + 1
            )
            generations_new = int(
                app.users_table.query_specific_user_data(
                    session["username"], "total_generations"
                )
            )
            assert generations_new == generations + 1
            print("should have successfully increment the total generations")
            # Decrement the tokens from the user
            username = session["username"]
            tokens = int(app.users_table.query_specific_user_data(username, "tokens"))
            app.users_table.edit_field_of_user(username, "tokens", tokens - 1)
            return send_file(
                buffer,
                as_attachment=True,
                download_name="cookie_cutter.stl",
                mimetype="model/stl",
            )

        return render_template("create.html")

    # @app.route("/confirm/<token>")
    # def confirm_email(token):
    #     try:
    #         email = self.s.loads(token, salt="email-confirm", max_age=3600)
    #     except Exception:
    #         flash("Invalid or expired link.")
    #         return render_template("login_user.html")

    #     ans = self.users_table.query_specific_user_data(email)
    #     if ans == []:
    #         flash("User not found.")
    #         return render_template("login_user.html")

    #     self.users_table.edit_field_of_user(email, "tokens", 5)
    #     self.users_table.edit_field_of_user(email, "email_verified", 1)
    #     flash(
    #         "Email Confirmed, please login. You have been granted 5x free tokens!"
    #     )
    #     self.frontend_link.redis.incr(TELEM_EMAIL_VERS)

    #     return render_template("login_user.html")
