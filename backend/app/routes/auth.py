from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db, bcrypt
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return jsonify({
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        })
    return jsonify({"error": "Not authenticated"}), 401
