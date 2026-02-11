from flask import Flask, render_template, request, redirect, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "blackchat_secret_key"

socketio = SocketIO(app)

# -------------------------
# In-Memory Storage (Temporary)
# -------------------------

users = {}  
# Structure:
# users = {
#   "username": {
#       "password": hashed_password,
#       "id": unique_id,
#       "online": False
#   }
# }

messages = []  
# Structure:
# {
#   "sender": username,
#   "receiver": username,
#   "message": text,
#   "timestamp": time
# }

# -------------------------
# Routes
# -------------------------

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

# -------------------------
# Socket Events
# -------------------------

@socketio.on("connect")
def handle_connect():
    print("User connected")


@socketio.on("join")
def handle_join(data):
    username = data["username"]
    join_room(username)
    emit("status", {"msg": f"{username} joined"}, broadcast=True)


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


@socketio.on("disconnect")
def handle_disconnect():
    print("User disconnected")

# -------------------------
# Run App
# -------------------------

if __name__ == "__main__":
    socketio.run(app, debug=True)