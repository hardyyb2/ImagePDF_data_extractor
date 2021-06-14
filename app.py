from flask import Flask, request, send_from_directory, render_template
from os import path
import logging

from extract_numbers import extract_phone_numbers

app = Flask(__name__)

if __name__ == "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.config["UPLOAD_FOLDER"] = "pdfs"
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(path.join(app.root_path, "static"), "favicon.ico")


@app.route("/phonenumbers", methods=["POST"])
def phonenumbers():
    app.logger.info(f"Received Request {request.method}")
    if request.method == "POST":
        f = request.files["file"]
        app.logger.info(f"File Name : {f.filename}")
        if f.filename == "":
            return "Please attach a PDF file"
        save_path = path.join("pdfs", f.filename)

        try:
            f.save((save_path))
            app.logger.info(f"Saved file {save_path}")
        except:
            err = "Failed to save file"
            app.logger.error(err)
            return err

        # Get phone number
        result = extract_phone_numbers(save_path)
        return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
