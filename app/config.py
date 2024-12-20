import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'dbdata', 'users.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set the secret key for session management
    # Replace 'super-secret-key' with something secure
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
