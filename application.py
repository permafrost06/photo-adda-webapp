import cs50
import re
import os
from flask import Flask, abort, redirect, render_template, request
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        filelist = []
        for file in request.files.getlist("file"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filelist.append(filename)
            file.close()
        return render_template("uploaded.html", files=filelist)
    else:
        """Handle requests for / via GET (and POST)"""
        return render_template("index.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        feed = open("static/feedback.txt", "a")
        feed.write("\n\n{}".format(request.form.get("feed")))
        if request.form.get("name"):
            feed.write("\n--{}".format(request.form.get("name")))
        else:
            feed.write("\n--<unknown>")
        feed.write("\n{}".format(datetime.now()))
        feed.close()
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", files=sorted(os.listdir("static/files/")))


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code

# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.run()