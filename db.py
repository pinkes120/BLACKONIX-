# ===============================
# BLACKONIX db.py
# Database Configuration
# ===============================

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()


# ===============================
# User Model
# ===============================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    messages = db.relationship("Message", backref="author", lazy=True)

    # Password Hash
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Check Password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"


# ===============================
# Message Model
# ===============================
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.id}>"