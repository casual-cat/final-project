from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    avatar_filename = db.Column(db.String(300), nullable=True)  # New field for PFP

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=True)  # New title field
    data = db.Column(db.String(300))     # Text data
    filename = db.Column(db.String(300)) # Uploaded file name (if any)

    user = db.relationship('User', backref='items', lazy=True)

