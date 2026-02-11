from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

from config import Config   # Config imported here

# ---------------------------------
# App Setup
# ---------------------------------

app = Flask(__name__)
app.config.from_object(Config)   # Config connected here

socketio = SocketIO(app, async_mode=app.config["SOCKETIO_ASYNC_MODE"])

# ---------------------------------
# Temporary Storage (Later MongoDB)
# ---------------------------------

users = {}
messages = []

# ---------------------------------
# Routes
# ---------------------------------

@app.route("/")
def home():
    if "username" in session:
        return redirect("/chat")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists!"

        hashed_password = generate_password_hash(password)

        users[username] = {
            "id": str(uuid.uuid4()),
            "password": hashed_password,
            "online": False
        }

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and check_password_hash(users[username]["password"], password):
        session["username"] = username
        users[username]["online"] = True
        return redirect("/chat")

    return "Invalid username or password"


@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect("/")
    return render_template("chat.html", username=session["username"], users=users)


@app.route("/logout")
def logout():
    username = session.get("username")
    if username in users:
        users[username]["online"] = False
    session.clear()
    return redirect("/")

# ---------------------------------
# Socket Events
# ---------------------------------

@socketio.on("join")
def handle_join(data):
    username = data["username"]
    join_room(username)


@socketio.on("private_message")
def handle_private_message(data):
    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]

    timestamp = datetime.now().strftime("%H:%M")

    msg_data = {
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": timestamp
    }

    messages.append(msg_data)

    emit("receive_message", msg_data, room=receiver)
    emit("receive_message", msg_data, room=sender)

# ---------------------------------
# Run Server
# ---------------------------------

if __name__ == "__main__":
    socketio.run(app, debug=True)