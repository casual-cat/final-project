from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure the dbdata directory exists
    db_path = os.path.join(app.root_path, 'dbdata')
    if not os.path.exists(db_path):
        os.makedirs(db_path)  # Create the directory if it doesn't exist

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import models AFTER db is initialized
    from app import models  # noqa: F401

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
