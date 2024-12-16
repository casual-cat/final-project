from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models import User, Item

main_bp = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        items = Item.query.filter_by(user_id=current_user.id).all()
        return render_template('home.html', items=items)
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('main.home'))
    return render_template('signup.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    # Example: just store the text in the DB
    data = request.form['data']
    new_item = Item(user_id=current_user.id, data=data)
    db.session.add(new_item)
    db.session.commit()
    flash('Uploaded successfully!')
    return redirect(url_for('main.home'))
