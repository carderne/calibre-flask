import os
import json
import yaml

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    send_from_directory,
)
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from werkzeug.security import check_password_hash

from .books import get_books

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)

users = yaml.safe_load(open("users.yaml"))


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = check_password_hash(users[username], request.form["pw"])
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    books = get_books()
    return render_template("index.html", books=json.dumps(books))


@app.route("/data/<path:path>")
@login_required
def get_dir(path):
    return send_from_directory("data", path)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    if check_password_hash(users[username], request.form["pw"]):
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for("index"))

    return "Bad login"


@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"
