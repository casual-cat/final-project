from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # You could add more fields (e.g. email, full_name, avatar, etc.)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(300))     # Text data
    filename = db.Column(db.String(300)) # Uploaded file name (if any)

    user = db.relationship('User', backref='items', lazy=True)
