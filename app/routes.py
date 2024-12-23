from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_from_directory, current_app
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Item
from . import db
import os

main = Blueprint('main', __name__)

@main.route("/")
def home():
    items = []
    if current_user.is_authenticated:
        items = Item.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", items=items)

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.home"))
        
        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("main.login"))

    return render_template("signup.html")

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # Update username
        new_username = request.form.get("username")
        if new_username:
            current_user.username = new_username

        # Update password if provided
        new_password = request.form.get("password")
        if new_password:
            current_user.set_password(new_password)

        # Handle avatar upload
        if request.files.get("avatar"):
            avatar = request.files["avatar"]
            avatar_filename = f"{current_user.id}_{avatar.filename}"
            avatar_path = os.path.join(current_app.root_path, "instance", avatar_filename)

            # Save the file in the instance folder
            avatar.save(avatar_path)
            current_user.avatar_filename = avatar_filename
            print(f"Avatar saved: {avatar_path}")  # Debug

        # Commit changes to the database
        db.session.commit()
        flash("Profile updated successfully!", "success")

    return render_template("profile.html")

@main.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    Route for the form in home.html: create a new item with optional file upload.
    """
    title = request.form.get("title")
    data = request.form.get("data")
    file_obj = request.files.get("file")

    new_item = Item(
        title=title,
        data=data,
        user_id=current_user.id
    )

    # If a file was uploaded, save it
    if file_obj and file_obj.filename:
        saved_name = f"{current_user.id}_{file_obj.filename}"
        save_path = os.path.join(current_app.root_path, "instance", saved_name)
        file_obj.save(save_path)
        new_item.filename = saved_name

    db.session.add(new_item)
    db.session.commit()

    flash("Item added successfully!", "success")
    return redirect(url_for("main.home"))

@main.route("/delete_item/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    """
    Handle AJAX-based deletion from home.html JS fetch.
    """
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'status': 'success'})

@main.route("/edit_item/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    """
    Load the item, ensure it belongs to current_user, allow editing.
    """
    item = Item.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Not authorized to edit this item.", "danger")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        new_title = request.form.get("title")
        new_data = request.form.get("data")
        item.title = new_title
        item.data = new_data
        db.session.commit()
        flash("Item updated successfully!", "success")
        return redirect(url_for("main.home"))

    return render_template("edit_item.html", item=item)

@main.route("/uploads/<filename>")
@login_required  # or remove this if you want public avatars
def uploaded_file(filename):
    """Serve uploaded files from the instance folder."""
    instance_folder = os.path.join(current_app.root_path, "instance")
    print(f"Serving file from: {instance_folder}, filename: {filename}")
    return send_from_directory(instance_folder, filename)
