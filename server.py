from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Server"


@app.route("/loadModel", method=["GET"])
def loadModel():
    if request.method == "GET":
        return "LoadModel"


@app.route("/inference", methods=["POST"])
def inference():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save("./" + filename)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)