import os

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.wrappers.response import Response

from .books import get_books

app = Flask(__name__)
PREFIX = os.getenv("BOOKS_PREFIX", "")
debug = app.config["DEBUG"]


@app.route(PREFIX + "/", methods=["GET", "POST"])
def index() -> str:
    s = request.form["s"] if request.method == "POST" else None
    books = get_books(search=s if s else "%")
    return render_template("basic.html", books=books, s=s)


@app.route(PREFIX + "/data/<path:path>")
def get_data(path: str) -> Response:
    return send_from_directory("data", path)
