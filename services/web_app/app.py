from flask import Flask, render_template  # request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return render_template("login.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/upload_image", methods=["POST"])
def upload_image():
    # data = request.get_json()

    return render_template("create.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
