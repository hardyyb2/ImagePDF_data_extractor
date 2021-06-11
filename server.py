from flask import Flask, request
from os import path

from extract_numbers import extract_phone_numbers

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "pdfs"


@app.route("/phonenumbers", methods=["POST"])
def phonenumbers():
    if request.method == "POST":
        f = request.files["file"]
        save_path = path.join("pdfs", f.filename)
        f.save(save_path)
        result = extract_phone_numbers(save_path)
        return result
