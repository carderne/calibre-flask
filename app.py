import json

from flask import Flask, render_template, redirect, url_for, request
import flask_login

from .books import get_books

app = Flask(__name__)
app.secret_key = "hello this is the secret_key for flask"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {"foo@bar.tld": {"pw": "secret"}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form["pw"] == users[email]["pw"]
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


@app.route("/")
@flask_login.login_required
def index():
    books = get_books()
    return render_template("index.html", books=json.dumps(books))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               """

    email = request.form["email"]
    if request.form["pw"] == users[email]["pw"]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for("index"))

    return "Bad login"


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"
