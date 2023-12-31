from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import local_config
import model.infer_retinanet as infer_retinanet


model_weights = 'model.t7'
recognizer = infer_retinanet.BrailleInference(
    params_fn=os.path.join(local_config.data_path, 'weights', 'param.txt'),
    model_weights_fn=os.path.join(local_config.data_path, 'weights', model_weights),
    create_script=None)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Server"


@app.route("/loadModel", method=["POST"])
def loadModel():
    if request.method == "POST":
        global recognizer
        recognizer = infer_retinanet.BrailleInference(
            params_fn=os.path.join(local_config.data_path, 'weights', 'param.txt'),
            model_weights_fn=os.path.join(local_config.data_path, 'weights', model_weights),
            create_script=None)


@app.route("/inference", methods=["POST"])
def inference():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save("./" + filename)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)