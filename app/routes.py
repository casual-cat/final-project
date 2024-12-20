import os
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, send_from_directory
)
from flask_login import (
    login_required, login_user, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import db, login_manager, ALLOWED_EXTENSIONS
from app.models import User, Item

main_bp = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    # Check if the extension is allowed
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('main.signup'))

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
<<<<<<< HEAD
    title = request.form.get('title')  # Get the title input
    data = request.form.get('data')  # Text data
    
=======
    data = request.form.get('data')  # Text data
>>>>>>> c66602dc39fe5156b4358f9b86cdd4b44d023233
    file = request.files.get('file')
    filename = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
<<<<<<< HEAD
        upload_path = os.path.join(main_bp.root_path, 'static', 'uploads', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
    
    new_item = Item(user_id=current_user.id, title=title, data=data, filename=filename)
=======
        upload_path = os.path.join(
            main_bp.root_path, 'static', 'uploads', filename
        )
        file.save(upload_path)

    new_item = Item(user_id=current_user.id, data=data, filename=filename)
>>>>>>> c66602dc39fe5156b4358f9b86cdd4b44d023233
    db.session.add(new_item)
    db.session.commit()
    flash('Item uploaded successfully!')
    return redirect(url_for('main.home'))


@main_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(main_bp.root_path, 'static', 'uploads'),
        filename
    )


@main_bp.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item and item.user_id == current_user.id:
        if item.filename:
            file_path = os.path.join(
                main_bp.root_path, 'static', 'uploads', item.filename
            )
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted.')
    else:
        flash('Item not found or not yours.')
    return redirect(url_for('main.home'))


@main_bp.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(item_id)
    if not item or item.user_id != current_user.id:
        flash("Item not found or not yours.")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        item.data = request.form.get('data')
        db.session.commit()
        flash('Item updated successfully!')
        return redirect(url_for('main.home'))

    return render_template('edit_item.html', item=item)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        if new_username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Username already taken by another user!')
                return redirect(url_for('main.profile'))
            current_user.username = new_username

        if new_password:
            current_user.password = generate_password_hash(new_password)

        file = request.files.get('avatar')
        if file and allowed_file(file.filename):
            avatar_name = secure_filename(file.filename)
            upload_path = os.path.join(
                main_bp.root_path, 'static', 'uploads', avatar_name
            )
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            current_user.avatar_filename = avatar_name

        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('main.profile'))

    return render_template('profile.html')
