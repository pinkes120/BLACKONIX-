from flask import Blueprint, request, jsonify, session
from model import db, User, Group
from datetime import datetime

chat = Blueprint("chat", __name__)

# ------------------------
# Message Model (Agar model.py me nahi hai to waha shift kar dena)
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
# Send Message
# ------------------------
@chat.route("/send/<int:group_id>", methods=["POST"])
def send_message(group_id):
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Message content required"}), 400

    user = User.query.get(session["user_id"])
    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    if user not in group.members:
        return jsonify({"error": "You are not a member of this group"}), 403

    new_message = Message(
        content=content,
        user_id=user.id,
        group_id=group.id
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent"}), 201


# ------------------------
# Get Messages
# ------------------------
@chat.route("/messages/<int:group_id>", methods=["GET"])
def get_messages(group_id):
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    messages = Message.query.filter_by(group_id=group_id).order_by(Message.timestamp.asc()).all()

    result = []
    for msg in messages:
        result.append({
            "id": msg.id,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "username": msg.user.username
        })

    return jsonify(result), 200