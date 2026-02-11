from flask import Blueprint, jsonify, request, session
from model import db, User
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__)

# ------------------------
# Get Current User Profile
# ------------------------
@user_bp.route("/me", methods=["GET"])
def get_current_user():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user = User.query.get(session["user_id"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }), 200


# ------------------------
# Get User by ID
# ------------------------
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at
    }), 200


# ------------------------
# Update Profile
# ------------------------
@user_bp.route("/update", methods=["PUT"])
def update_user():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user = User.query.get(session["user_id"])
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username:
        user.username = username

    if email:
        user.email = email

    if password:
        user.password = generate_password_hash(password)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200


# ------------------------
# Delete Account
# ------------------------
@user_bp.route("/delete", methods=["DELETE"])
def delete_user():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user = User.query.get(session["user_id"])

    db.session.delete(user)
    db.session.commit()

    session.pop("user_id", None)

    return jsonify({"message": "Account deleted successfully"}), 200