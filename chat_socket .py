from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import session
from model import db, User, Group
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*")


# ------------------------
# Message Model (Agar model.py me already hai to yeh remove karo)
# ------------------------
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

    user = db.relationship("User", backref="messages")
    group = db.relationship("Group", backref="messages")


# ------------------------
# Connect Event
# ------------------------
@socketio.on("connect")
def handle_connect():
    if "user_id" not in session:
        return False  # Reject connection

    print("User connected")


# ------------------------
# Join Group Room
# ------------------------
@socketio.on("join_group")
def handle_join(data):
    group_id = data.get("group_id")

    if "user_id" not in session:
        return

    group = Group.query.get(group_id)
    user = User.query.get(session["user_id"])

    if not group or user not in group.members:
        return

    room = f"group_{group_id}"
    join_room(room)

    emit("status", {"msg": f"{user.username} joined the group"}, room=room)


# ------------------------
# Leave Group
# ------------------------
@socketio.on("leave_group")
def handle_leave(data):
    group_id = data.get("group_id")
    room = f"group_{group_id}"

    leave_room(room)
    emit("status", {"msg": "User left the group"}, room=room)


# ------------------------
# Send Message
# ------------------------
@socketio.on("send_message")
def handle_message(data):
    if "user_id" not in session:
        return

    content = data.get("content")
    group_id = data.get("group_id")

    user = User.query.get(session["user_id"])
    group = Group.query.get(group_id)

    if not group or user not in group.members:
        return

    # Save message to DB
    new_message = Message(
        content=content,
        user_id=user.id,
        group_id=group.id
    )

    db.session.add(new_message)
    db.session.commit()

    room = f"group_{group_id}"

    emit("receive_message", {
        "username": user.username,
        "content": content,
        "timestamp": str(datetime.utcnow())
    }, room=room)


# ------------------------
# Disconnect Event
# ------------------------
@socketio.on("disconnect")
def handle_disconnect():
    print("User disconnected")