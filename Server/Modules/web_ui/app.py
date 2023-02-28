
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, send
from waitress import serve

app = Flask(__name__)
app.secret_key = b'\x9d\x97Leel\xe1\x15o\xd9:\xe8'
socketio = SocketIO(app, cors_allowed_origins="*")

def start():
    serve(app, host="0.0.0.0", port=5000) # pro dev: flask run --host=0.0.0.0

class AuthStore():
    def login(username:str, password:str):
        session["username"] = username
        session["password"] = password

    def register(email:str, username:str, password:str, repeat_password:str):
        session["username"] = username
        session["password"] = password

    def logout():
        session["username"] = ""
        session["password"] = ""

    def is_logged():
        if session["password"] == "" or session["password"] == "": return False
        else: return True

@app.route("/")
def index():
    return redirect(url_for('login'))
    #flash("Ahoj")
    #return render_template("index.html")

@app.route("/login")
def login():
    return render_template("user/login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    if username and password: AuthStore.login(username, password)

    if AuthStore.is_logged:
        return redirect(url_for('home'))
    
    return render_template("user/login.html")

@app.route("/register")
def register():
    return render_template("user/register.html")

@app.route("/register", methods=["POST"])
def regiter_post():
    email = "mail xD"
    username = request.form["username"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    
    if username and password and password == repeat_password: AuthStore.register(email, username, password, repeat_password)

    if AuthStore.is_logged:
        return redirect(url_for('home'))
    
    return render_template("user/register.html")

@app.route("/home")
def home():
    if AuthStore.is_logged:
        return render_template("user/home/home.html")

    return redirect(url_for('login'))

"""
@app.route("/home/settings")
def settings():
    if AuthStore.is_logged:
        return "Ok"

    return redirect(url_for('login'))
"""

@app.route("/home/chat")
def chat():
    if AuthStore.is_logged:
        return render_template("user/home/chat.html")

    return redirect(url_for('login'))

@app.route("/home/voice")
def voice():
    if AuthStore.is_logged:
        return render_template("user/home/voice.html")

    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(message):
    print(f'New message: {message}')
    if message != "User connected!":
        send(message, broadcast=True)

@app.route('/')
def sessions():
    return render_template('user/home/chat.html')


if __name__ == "__main__": start()