from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId


class UserModel:

    def __init__(self, db):
        self.collection = db["users"]

    # ---------------------------------
    # Create New User
    # ---------------------------------
    def create_user(self, username, password):
        if self.collection.find_one({"username": username}):
            return False

        hashed_password = generate_password_hash(password)

        user_data = {
            "username": username,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "online": False,
            "last_seen": None,
            "profile_pic": None,
            "blocked_users": []
        }

        self.collection.insert_one(user_data)
        return True

    # ---------------------------------
    # Verify Login
    # ---------------------------------
    def verify_user(self, username, password):
        user = self.collection.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            return True

        return False

    # ---------------------------------
    # Get User
    # ---------------------------------
    def get_user(self, username):
        return self.collection.find_one({"username": username}, {"password": 0})

    # ---------------------------------
    # Set Online
    # ---------------------------------
    def set_online(self, username):
        self.collection.update_one(
            {"username": username},
            {"$set": {"online": True}}
        )

    # ---------------------------------
    # Set Offline
    # ---------------------------------
    def set_offline(self, username):
        self.collection.update_one(
            {"username": username},
            {"$set": {
                "online": False,
                "last_seen": datetime.utcnow()
            }}
        )

    # ---------------------------------
    # Block User
    # ---------------------------------
    def block_user(self, username, block_username):
        self.collection.update_one(
            {"username": username},
            {"$addToSet": {"blocked_users": block_username}}
        )

    # ---------------------------------
    # Unblock User
    # ---------------------------------
    def unblock_user(self, username, unblock_username):
        self.collection.update_one(
            {"username": username},
            {"$pull": {"blocked_users": unblock_username}}
        )