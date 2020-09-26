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
app.config.from_pyfile("../config.py")

login_manager = LoginManager()
login_manager.init_app(app)

users = yaml.safe_load(open("users.yaml"))
debug = app.config["DEBUG"]
book_lim = 50 if debug else None


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
    return redirect(
        url_for(
            "login", msg="You must log in!", d=request.endpoint, s=request.args.get("s")
        )
    )


@app.route("/")
@login_required
def index():
    books = get_books(lim=book_lim)
    return render_template("index.html", books=books)


@app.route("/b/", methods=["GET", "POST"])
@login_required
def basic():
    s = None
    if request.method == "POST":
        s = request.form["s"]
    books = get_books(lim=book_lim, search=s)
    return render_template("basic.html", books=books, s=s)


@app.route("/data/<path:path>")
@login_required
def get_data(path):
    return send_from_directory("data", path)


@app.route("/resized/<path:path>")
def get_img(path):
    return send_from_directory("resized", path)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        msg = request.args.get("msg")
        msg = msg if msg else ""
        return render_template("login.html", msg=msg)

    username = request.form["username"]
    if check_password_hash(users[username], request.form["pw"]):
        user = User()
        user.id = username
        login_user(user)
        dest = request.args.get("d")
        dest = dest if dest else "index"
        return redirect(url_for(dest, s=request.args.get("s")))

    return redirect(
        url_for(
            "login", msg="Bad login!", d=request.args.get("d"), s=request.args.get("s")
        )
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login", msg="You've logged out!", d=request.args.get("d")))
