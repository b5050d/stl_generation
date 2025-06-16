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
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import os
import io
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

from utils.frontend_link import FrontendLink
from utils.database_methods import UsersTable
from utils.helper_methods import is_valid_email, is_password_strong
from utils.routes import init_routes

from mock import MagicMock



class AppFactory:
    """
    Class to handle web app creation,

    makes it a lot easier to mock out things that need to get mocked out
    """

    def __init__(self):
        """
        Set up the app
        """
        self.define_config()

    def define_config(self):
        """
        Define the config to use in the app
        """
        self.config = {
            "TELEM_ATTEMPT_GEN": "telem:1",
            "TELEM_SUCCESS_GEN": "telem:2",
            "TELEM_FAILURE_GEN": "telem:3",
            "TELEM_SIGNUPS": "telem:4",
            "TELEM_LOGINS": "telem:5",
            "TELEM_LOGOUTS": "telem:6",
            "TELEM_EMAIL_VERS": "telem:7",
            "SECRET_KEY": os.getenv("SECRET_KEY", "random_secret_key"),
            "MAIL_SERVER": "smtp.sendgrid.net",
            "MAIL_PORT": 587,
            "MAIL_USE_TLS": True,
            "MAIL_USERNAME": "apikey",
            "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD", "no_password_provided"),
            "MAIL_DEFAULT_SENDER": "no-reply@yourdomain.com",
            "DATABASE_PATH": os.getenv("DATABASE_PATH", "/app/app_data/sample.db"),
        }

    def create_app(self, test = False):
        """
        Create the actual Flask app and return the app as an obj
        """
        self.app = Flask(__name__, static_folder="static")
        self.app.config.update(self.config)

        if test: self._mock_connections(test)
        else: self._set_up_connections()
        
        self._set_up_routes()

        return self.app

    def _set_up_connections(self):
        """
        Set up the connections to necessary interfaces

        Can be abstracted out for test purposes
        """
        self.app.frontend_link = FrontendLink()
        self.app.mail = Mail(self.app)
        self.app.s = URLSafeTimedSerializer(self.app.config["SECRET_KEY"])

        database_path = self.app.config["DATABASE_PATH"]
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        self.app.users_table = UsersTable(database_path)

    def _mock_connections(self, test_path):
        """
        Set up mocked connections

        Hint provide test_path as the path to the test database
        """
        self.app.frontend_link = MagicMock()
        self.app.mail = MagicMock()

        # The following Doesnt need to be mocked
        self.app.s = URLSafeTimedSerializer(self.app.config["SECRET_KEY"])

        database_path = test_path
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        self.app.users_table = UsersTable(database_path)

    def _set_up_routes(self):
        """
        Set up the routes
        """
        init_routes(self.app)


# class AppMaker:
#     """
#     Provision the application object for use
#     Creating this as a class for ease of testing
#     """

#     def __init__(self, test=False):
#         if test:
#             self.frontend_link = MagicMock()
#         else:
#             # Establish link to the backend
#             self.frontend_link = FrontendLink()

#         self.app = Flask(__name__, static_folder="static")
#         self.app.secret_key = os.getenv("SECRET_KEY", "random_secret_key")

#         # Set up the Email Verification
#         self.app.config.update(
#             MAIL_SERVER="smtp.sendgrid.net",
#             MAIL_PORT=587,
#             MAIL_USE_TLS=True,
#             MAIL_USERNAME="apikey",  # this is literally the word 'apikey'
#             MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "no_password_provided"),
#             MAIL_DEFAULT_SENDER="no-reply@yourdomain.com",
#         )
#         self.mail = Mail(self.app)
#         self.s = URLSafeTimedSerializer(self.app.config["SECRET_KEY"])

#         # Set up the Database
#         DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/app_data/sample.db")
#         database_folder = os.path.dirname(DATABASE_PATH)
#         os.makedirs(database_folder, exist_ok=True)  # Create the folder if it DNE
#         self.users_table = UsersTable(DATABASE_PATH)

#     def define_routes(self):
#         # Wrapper function to ensure log in to specfic features
#         def login_required(f):
#             @wraps(f)
#             def decorated_function(*args, **kwargs):
#                 if "username" not in session:
#                     flash("Please log in to access this page.", "warning")
#                     return redirect(url_for("login"))
#                 return f(*args, **kwargs)

#             return decorated_function

#         def force_log_out(f):
#             @wraps(f)
#             def decorated_function(*args, **kwargs):
#                 if "username" in session:
#                     flash(f"Logged {session['username']} out", "warning")
#                     session.pop("username")
#                     return redirect(url_for("login"))
#                 return f(*args, **kwargs)

#             return decorated_function

#         @self.app.route("/")
#         def index():
#             return render_template("home.html")

#         @self.app.route("/login", methods=["GET", "POST"])
#         @force_log_out
#         def login():
#             if request.method == "POST":
#                 print("Got a post request!")
#                 username = request.form.get("username", "").strip()
#                 expected_password_hash = self.users_table.query_specific_user_data(
#                     username, "password_hash"
#                 )

#                 if expected_password_hash == []:
#                     flash("User not found")
#                     return render_template("login_user.html")

#                 if check_password_hash(
#                     expected_password_hash, request.form.get("password", "").strip()
#                 ):
#                     print("Correct Password!!!")
#                     session["username"] = username
#                     flash("Login Successful!", "success")
#                     self.frontend_link.redis.incr(TELEM_LOGINS)
#                     return redirect(url_for("create"))
#                 else:
#                     flash("Incorrect password.", "danger")

#             return render_template("login_user.html")

#         @self.app.route("/logout")
#         def logout():
#             if "username" in session:
#                 session.pop("username", None)
#                 flash("You have been logged out.", "info")
#                 self.frontend_link.redis.incr(TELEM_LOGOUTS)
#             else:
#                 flash("No user was logged in to log out")
#             return redirect(url_for("login"))

#         @self.app.route("/confirm/<token>")
#         def confirm_email(token):
#             try:
#                 email = self.s.loads(token, salt="email-confirm", max_age=3600)
#             except Exception:
#                 flash("Invalid or expired link.")
#                 return render_template("login_user.html")

#             ans = self.users_table.query_specific_user_data(email)
#             if ans == []:
#                 flash("User not found.")
#                 return render_template("login_user.html")

#             self.users_table.edit_field_of_user(email, "tokens", 5)
#             self.users_table.edit_field_of_user(email, "email_verified", 1)
#             flash(
#                 "Email Confirmed, please login. You have been granted 5x free tokens!"
#             )
#             self.frontend_link.redis.incr(TELEM_EMAIL_VERS)

#             return render_template("login_user.html")

#         @self.app.route("/register", methods=["GET", "POST"])
#         def register():
#             if request.method == "POST":
#                 username = request.form.get("username", "").strip()

#                 # TODO - Add a better method for checking whether an email address is valid
#                 if not is_valid_email(username):
#                     flash("Must provide valid email address!")
#                     return render_template("register_user.html")

#                 # Check that the username is not already in the database
#                 ans = self.users_table.query_specific_user_data(username, "id")
#                 if ans != []:
#                     flash("Error: Username is already in use!")
#                     return render_template("register_user.html")

#                 if not is_password_strong(request.form.get("password1", "")):
#                     flash(
#                         "Error! Password Does not meet complexity requirements. Must be length >8, 1x digit, 1x special char, 1x uppercase, 1x lowercase"
#                     )
#                     return render_template("register_user.html")

#                 password1 = generate_password_hash(
#                     request.form.get("password1", "").strip()
#                 )
#                 if not check_password_hash(
#                     password1, request.form.get("password2", "").strip()
#                 ):
#                     flash("Passwords don't match!")
#                     return render_template("register_user.html")
#                 else:
#                     # TODO - Check that the username is a valid email
#                     # Check that the user is not already present
#                     self.users_table.add_user(username, password1)

#                     print("Added user to the user table!")
#                     flash(
#                         "Successfully added user! Please verify your email before you can login"
#                     )
#                     self.frontend_link.redis.incr(TELEM_SIGNUPS)

#                     # Send the email to verify the account
#                     verification_token = self.s.dumps(username, salt="email-confirm")
#                     link = url_for(
#                         "confirm_email", token=verification_token, _external=True
#                     )
#                     msg = Message("Confirm Your Email", recipients=[username])
#                     msg.body = f"Click the link to confirm your email: {link}"
#                     self.mail.send(msg)

#                     return render_template("login_user.html")

#             return render_template("register_user.html")

#         @self.app.route("/create")
#         @login_required
#         def create():
#             return render_template("create.html")

#         @self.app.route("/upload_image", methods=["POST"])
#         @login_required
#         def upload_image():
#             print("I got an image bro!")

#             data = request.get_json()
#             if data:
#                 print("Received data from JS")
#                 self.frontend_link.redis.incr(TELEM_ATTEMPT_GEN)
#                 base64_image_data = data["image_data"]
#                 image_bytes = base64.b64decode(base64_image_data)

#                 print("Contacting the Backend")
#                 data = self.frontend_link.publish_message(image_bytes)
#                 print("Got Response from the backend")

#                 # 2️⃣ Wrap in a BytesIO object
#                 buffer = io.BytesIO(data)
#                 buffer.seek(0)

#                 # 3️⃣ Use send_file to let the browser download it

#                 # increment the generationrs counter
#                 print("Attempting to increment the counter for total generations")
#                 generations = int(
#                     self.users_table.query_specific_user_data(
#                         session["username"], "total_generations"
#                     )
#                 )
#                 self.users_table.edit_field_of_user(
#                     session["username"], "total_generations", generations + 1
#                 )
#                 generations_new = int(
#                     self.users_table.query_specific_user_data(
#                         session["username"], "total_generations"
#                     )
#                 )
#                 assert generations_new == generations + 1
#                 print("should have successfully increment the total generations")
#                 # Decrement the tokens from the user
#                 username = session["username"]
#                 tokens = int(
#                     self.users_table.query_specific_user_data(username, "tokens")
#                 )
#                 self.users_table.edit_field_of_user(username, "tokens", tokens - 1)
#                 return send_file(
#                     buffer,
#                     as_attachment=True,
#                     download_name="cookie_cutter.stl",
#                     mimetype="model/stl",
#                 )

#             return render_template("create.html")

#         @self.app.route("/account", methods=["GET", "POST"])
#         @login_required
#         def account():
#             # Get the information from the user from the database
#             username = session["username"]

#             total_genearations = self.users_table.query_specific_user_data(
#                 username, "total_generations"
#             )
#             tokens_remaining = self.users_table.query_specific_user_data(
#                 username, "tokens"
#             )
#             date_joined = self.users_table.query_specific_user_data(
#                 username, "date_joined"
#             )

#             user_data = {}
#             user_data["username"] = ("Username", username)
#             user_data["total_generations"] = (
#                 "Total Files Generated",
#                 total_genearations,
#             )
#             user_data["tokens_remaining"] = ("Tokens Remaining", tokens_remaining)
#             user_data["date_joined"] = ("Date Joined", date_joined)

#             # clean the date

#             return render_template("account.html", user_data=user_data)

#         @self.app.route("/reset_request", methods=["POST"])
#         def reset_request():
#             email = request.form["email"]
#             ans = self.users_table.query_specific_user_data(email)
#             if ans == []:
#                 flash("User not found")
#                 return render_template("reset_request.html")
#             else:
#                 token = self.s.dumps(email, salt="password-reset")
#                 link = url_for("reset_token", token=token, _external=True)
#                 msg = Message("Reset Your Password", recipients=[email])
#                 msg.body = f"Click to reset your password: {link}"
#                 self.mail.send(msg)
#             return "Check your email for a password reset link."

#         @self.app.route("/reset/<token>", methods=["GET", "POST"])
#         def reset_token(token):
#             try:
#                 email = self.s.loads(token, salt="password-reset", max_age=3600)
#             except Exception:
#                 return "Invalid or expired token."

#             ans = self.users_table.query_specific_user_data(email)
#             if ans == []:
#                 flash("User not found.")
#                 return render_template("home.html")

#             if request.method == "POST":
#                 new_password = generate_password_hash(request.form["password"])
#                 self.users_table.edit_field_of_user(
#                     email, "password_hash", new_password
#                 )
#                 flash("Password updated.")
#                 return render_template("login_user.html")

#             flash("Error, you shouldn't be able to get here")
#             return render_template("login_user.html")


if __name__ == "__main__":
    app_class = WebApp()
    app_class.app.run(host="127.0.0.1", port=5000, debug=True)
