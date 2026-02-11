import os

class Config:
    # ---------------------------------
    # Basic App Configuration
    # ---------------------------------
    SECRET_KEY = "blackchat_super_secret_key"
    DEBUG = True

    # ---------------------------------
    # MongoDB Configuration (Future Use)
    # ---------------------------------
    MONGO_URI = "mongodb://localhost:27017/blackchat"

    # ---------------------------------
    # JWT Authentication (Future Upgrade)
    # ---------------------------------
    JWT_SECRET_KEY = "blackchat_jwt_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # ---------------------------------
    # File Upload Settings
    # ---------------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

    # ---------------------------------
    # SocketIO Settings
    # ---------------------------------
    SOCKETIO_ASYNC_MODE = "threading"

    # ---------------------------------
    # Security Settings
    # ---------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Change to True in production (HTTPS)