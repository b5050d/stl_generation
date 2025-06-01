from flask import Flask, render_template, request
import base64
from io import BytesIO
import cv2
import numpy as np
from matplotlib import pyplot as plt
import redis

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login_user.html")

@app.route("/logout")
def logout():
    return render_template("login_user.html")

@app.route("/register")
def register():
    return render_template("register_user.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/upload_image", methods=["POST"])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
