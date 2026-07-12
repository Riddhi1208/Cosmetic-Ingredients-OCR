from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from ocr import extract_ingredients
from safety import get_functions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["image"]
    skin_type = request.form.get("skin_type")

    if file.filename == "":
        return jsonify({"error": "Empty file"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        #Run OCR 
        ingredients = extract_ingredients(filepath)

        #analysing ingredients
        functions = get_functions(ingredients)

        return jsonify({
            "ingredients": ingredients,
            "functions": functions
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)