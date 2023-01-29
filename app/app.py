import yaml
from flask import (
    Flask,
    Request,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import (  # type: ignore[import]
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash
from werkzeug.wrappers.response import Response

from .books import get_books

PREFIX = "/books"

app = Flask(__name__)
app.config.from_pyfile("../config.py")

login_manager = LoginManager()
login_manager.init_app(app)

if not app.config["LOGIN_DISABLED"]:
    users = yaml.safe_load(open("users.yaml"))
else:
    users = []
debug = app.config["DEBUG"]
book_lim = 50 if debug else -1

limited_user_agents = ["Kindle", "Kobo"]


class User(UserMixin):  # type: ignore[no-any-unimported]
    pass


@login_manager.user_loader
def user_loader(username: str) -> User | None:
    if username not in users:
        return None
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request: Request) -> User | None:
    username = request.form.get("username")
    if username not in users:
        return None
    user = User()
    user.id = username
    try:
        user.is_authenticated = check_password_hash(users[username], request.form["pw"])
    except KeyError:
        user.is_authenticated = False
    return user


@login_manager.unauthorized_handler
def unauthorized_handler() -> Response:
    return redirect(url_for("login", msg="You must log in!", s=request.args.get("s")))


@app.route(PREFIX + "/", methods=["GET", "POST"])
@login_required
def index() -> str:
    s = request.form["s"] if request.method == "POST" else None
    books = get_books(lim=book_lim, search=s if s else "%")
    return render_template("basic.html", books=books, s=s)


@app.route(PREFIX + "/b/")
@login_required
def basic() -> Response:
    return redirect(url_for("index"), code=301)


@app.route(PREFIX + "/data/<path:path>")
@login_required
def get_data(path: str) -> Response:
    return send_from_directory("data", path)


@app.route(PREFIX + "/resized/<path:path>")
def get_img(path: str) -> Response:
    return send_from_directory("resized", path)


@app.route(PREFIX + "/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "GET":
        msg = request.args.get("msg")
        msg = msg if msg else ""
        return render_template("login.html", msg=msg)

    username = request.form["username"]
    try:
        auth = check_password_hash(users[username], request.form["pw"])
    except KeyError:
        auth = False
    if auth:
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for("index", s=request.args.get("s")))

    return redirect(
        url_for(
            "login", msg="Bad login!", d=request.args.get("d"), s=request.args.get("s")
        )
    )


@app.route(PREFIX + "/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("login", msg="You've logged out!"))
