
from flask import Flask, render_template, request, flash, redirect, url_for, session
from Modules.engine.engine import *
from Modules.user_manager.user_manager import *
from waitress import serve

app = Flask(__name__)
app.secret_key = b'\x9d\x97Leel\xe1\x15o\xd9:\xe8'

def start():
    serve(app, host="0.0.0.0", port=5000) # pro dev: flask run --host=0.0.0.0

class AuthManager():
    def login(username:str, password:str):
        user = AuthStore.login(username, password)
        if user["status"] == "ok":
            session["username"] = username
            session["password"] = password
        else:
            session["username"] = ""
            session["password"] = ""

    def register(username:str, password:str):
        user = AuthStore.register(username, password)
        if user["status"] == "ok":
            session["username"] = username
            session["password"] = password
        else:
            session["username"] = ""
            session["password"] = ""

    def logout():
        session["username"] = ""
        session["password"] = ""

    def is_logged():
        try:
            if session["username"] == "" or session["password"] == "": return False
            else: return True
        except: return False

    def user():
        data = {}
        data["username"] = session["username"]
        data["password"] = session["password"]
        return data

@app.route("/") ##############################    Default    ##############################
def index():
    return redirect(url_for('login'))

@app.route("/login") ##############################    Login    ##############################
def login():
    return render_template("user/login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    if username and password: AuthManager.login(username, password)

    if AuthManager.is_logged():
        return redirect(url_for('home'))
    
    return render_template("user/login.html")

@app.route("/register") ##############################    Register    ##############################
def register():
    return render_template("user/register.html")

@app.route("/register", methods=["POST"])
def regiter_post():
    email = "mail xD"
    username = request.form["username"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    
    if username and password and password == repeat_password: AuthManager.register(username, password)

    if AuthManager.is_logged():
        return redirect(url_for('home'))
    
    return render_template("user/register.html")

@app.route("/logout") ##############################    Logout    ##############################
def logout():
    AuthManager.logout()
    return redirect(url_for("login"))

@app.route("/home") ##############################    Home    ##############################
def home():
    if AuthManager.is_logged():
        return render_template("user/home/home.html")

    return redirect(url_for('login'))

"""
@app.route("/home/settings")
def settings():
    if AuthManager.is_logged():
        return "Ok"

    return redirect(url_for('login'))
"""

@app.route("/home/chat") ##############################    Chat    ##############################
def chat():
    session["messages_from_server"] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    session["messages_from_user"] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    if AuthManager.is_logged():
        user = AuthManager.user()

        flash(user["username"])

        return render_template("user/home/chat.html")

    return redirect(url_for('login'))

@app.route("/home/chat", methods=["POST"])
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
            for i in user_mes: flash(i)
            for i in server_mes: flash(i)

            return render_template("user/home/chat.html")
        
        else:
            user = AuthManager.user()

            user_mes = session["messages_from_user"]
            server_mes = session["messages_from_server"]

            flash(user["username"])
            for i in user_mes: flash(i)
            for i in server_mes: flash(i)

            return render_template("user/home/chat.html")

    return redirect(url_for('login'))

@app.route("/home/voice") ##############################    Voice    ##############################
def voice():
    if AuthManager.is_logged():
        return render_template("user/home/voice.html")

    return redirect(url_for('login'))
