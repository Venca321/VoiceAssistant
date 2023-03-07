
from flask import Flask, render_template, request, flash, redirect, url_for, session
from Modules.engine.engine import *
from Modules.user_manager.user_manager import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from waitress import serve
import configparser, os, smtplib, ssl

config = configparser.ConfigParser(allow_no_value=True)
config.read(f"{os.getcwd()}/Data/config.ini")

secret = configparser.ConfigParser(allow_no_value=True)
secret.read(f"{os.getcwd()}/Modules/web_ui/data/secret.ini")

app = Flask(__name__)
app.secret_key = b'\x9d\x97Leel\xe1\x15o\xd9:\xe8'


def start():
    serve(app, host="0.0.0.0", port=5000)  # pro dev: flask run --host=0.0.0.0
    # serve(app, host="localhost", port=5000) #ngrok http 5000


class AuthManager():
    def clear():
        session["username"] = ""
        session["password"] = ""

    def login(username: str, password: str):
        if not username:
            AuthManager.clear()
            return "Zadejte uživatelské jméno"

        if not password:
            AuthManager.clear()
            return "Zadejte heslo"

        user = AuthStore.login(username, password)
        if user["status"] == "ok":
            session["username"] = username
            session["password"] = password
        else:
            AuthManager.clear()
            return "Neplatné uživatelské jméno nebo heslo"

    def register(username: str, email: str, password: str, repeat_password: str):
        if not email == "alfa-tester@token.cz":
            AuthManager.clear()
            return "Neplatný alfa token"

        if not username or len(username) < 4 or " " in username:
            AuthManager.clear()
            return "Neplatné uživatelské jméno"

        if not password or len(password) < 8 or " " in password:
            AuthManager.clear()
            return "Neplatné heslo"

        if not password == repeat_password:
            AuthManager.clear()
            return "Hesla se neshodují"

        user = AuthStore.register(username, password)
        if user["status"] == "ok":
            session["username"] = username
            session["password"] = password
        else:
            AuthManager.clear()
            return "Error"

    def logout():
        session["username"] = ""
        session["password"] = ""

    def is_logged():
        try:
            if session["username"] == "" or session["password"] == "":
                return False
            else:
                return True
        except:
            return False

    def user():
        data = {}
        data["username"] = session["username"]
        data["password"] = session["password"]
        return data


def sendmail(user: dict, subject: str, message: str):
    receiver_email = secret.get("Login", "email_to")
    sender_email = secret.get("Login", "email")
    password = secret.get("Login", "password")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg.attach(MIMEText(f"{user['username']}: \n{message}", 'plain', 'utf-8')) 

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# Default    ##############################
@app.route("/", strict_slashes=False)
def index():
    return redirect(url_for('login'))


# Login    ##############################
@app.route("/login", strict_slashes=False)
def login():
    flash(config.get("Info", "version"))
    return render_template("user/auth/login.html")


@app.route("/login", strict_slashes=False, methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    error = AuthManager.login(username, password)

    if AuthManager.is_logged():
        return redirect(url_for('home'))

    flash(config.get("Info", "version"))
    flash(error)
    return render_template("user/auth/login.html")


# Register    ##############################
@app.route("/register", strict_slashes=False)
def register():
    flash(config.get("Info", "version"))
    return render_template("user/auth/register.html")


@app.route("/register", strict_slashes=False, methods=["POST"])
def regiter_post():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]

    error = AuthManager.register(username, email, password, repeat_password)

    if AuthManager.is_logged():
        return redirect(url_for('home'))

    flash(config.get("Info", "version"))
    flash(error)
    return render_template("user/auth/register.html")


# Logout    ##############################
@app.route("/logout", strict_slashes=False)
def logout():
    AuthManager.logout()
    return redirect(url_for("login"))


# Home    ##############################
@app.route("/home", strict_slashes=False)
def home():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/home/home.html")

    return redirect(url_for('login'))


# Settings    ##############################
@app.route("/home/settings", strict_slashes=False)
def settings():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/settings/settings.html")

    return redirect(url_for('login'))


# Chat    ##############################
@app.route("/home/chat", strict_slashes=False)
def chat():
    session["messages_from_server"] = ["", "", "", "", "", "",
                                       "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    session["messages_from_user"] = ["", "", "", "", "", "",
                                     "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])

        return render_template("user/home/chat.html")

    return redirect(url_for('login'))


@app.route("/home/chat", strict_slashes=False, methods=["POST"])
def chat_post():
    message = request.form["message"]

    if AuthManager.is_logged():
        if message:
            user = AuthManager.user()

            user_mes = session["messages_from_user"]
            user_mes.remove(user_mes[0])
            user_mes.append(message)

            server_mes = session["messages_from_server"]
            server_mes.remove(server_mes[0])
            server_mes.append(Engine.process(user, message))

            session["messages_from_user"] = user_mes
            session["messages_from_server"] = server_mes

            flash(user["username"])
            for i in user_mes:
                flash(i)
            for i in server_mes:
                flash(i)

            return render_template("user/home/chat.html")

        else:
            user = AuthManager.user()

            user_mes = session["messages_from_user"]
            server_mes = session["messages_from_server"]

            flash(user["username"])
            for i in user_mes:
                flash(i)
            for i in server_mes:
                flash(i)

            return render_template("user/home/chat.html")

    return redirect(url_for('login'))


# Voice    ##############################
@app.route("/home/voice", strict_slashes=False)
def voice():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/home/voice.html")

    return redirect(url_for('login'))


# Contact    ##############################
@app.route("/home/contact", strict_slashes=False)
def contact():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/contact/contact.html")

    return redirect(url_for('login'))


# BugReport    ##############################
@app.route("/home/bugreport", strict_slashes=False)
def bugreport():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/contact/bugreport.html")

    return redirect(url_for('login'))


@app.route("/home/bugreport", strict_slashes=False, methods=["POST"])
def bugreport_post():
    message = request.form["message"]
    if AuthManager.is_logged():
        if message:
            user = AuthManager.user()

            sendmail(user, "New bug reported!", message)

            flash(user["username"])
            return render_template("user/contact/bugreport.html")

    return redirect(url_for('login'))


# FeatureRequest    ##############################
@app.route("/home/featurerequest", strict_slashes=False)
def featurerequest():
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])
        return render_template("user/contact/featurerequest.html")

    return redirect(url_for('login'))


@app.route("/home/featurerequest", strict_slashes=False, methods=["POST"])
def featurerequest_post():
    message = request.form["message"]
    if AuthManager.is_logged():
        if message:
            user = AuthManager.user()

            sendmail(user, "New feature request!", message)

            flash(user["username"])
            return render_template("user/contact/featurerequest.html")

    return redirect(url_for('login'))
