import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from BrailleToKor import BrailleToKor
import local_config
import model.infer_retinanet as infer_retinanet

model_weights = 'model.t7'
recognizer = infer_retinanet.BrailleInference(
    params_fn=os.path.join(local_config.data_path, 'weights', 'param.txt'),
    model_weights_fn=os.path.join(local_config.data_path, 'weights', model_weights),
    create_script=None)
translator = BrailleToKor()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Server"


@app.route("/loadModel", methods=["POST"])
def loadModel():
    if request.method == "POST":
        global recognizer, translator
        recognizer = infer_retinanet.BrailleInference(
            params_fn=os.path.join(local_config.data_path, 'weights', 'param.txt'),
            model_weights_fn=os.path.join(local_config.data_path, 'weights', model_weights),
            create_script=None)
        translator = BrailleToKor()
        return "LoadModel"


@app.route("/inference", methods=["POST"])
def inference():
    if request.method == "POST":
        global recognizer, translator
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save("./" + filename)
        path = os.getcwd() + "\\" + filename
        print(path)
        braille_texts = recognizer.inference(filename, lang="RU",
                                      draw_refined=recognizer.DRAW_NONE,
                                      find_orientation=True,
                                      process_2_sides=False,
                                      align_results=True,
                                      repeat_on_aligned=False)
        
        translated_texts = []
        if braille_texts is None:
            src_text = ""
            translated_text = ""
        else:
            src_text = "\n".join(braille_texts)
            for line in braille_texts:
                translated_texts.append(translator.translation(line)) 
            translated_text = "\n".join(translated_texts)
            
        return jsonify({"srcText": src_text, "translatedText": translated_text})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)