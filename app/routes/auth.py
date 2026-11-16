from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400
    if "@" not in email:
        return jsonify({"error": "enter a valid email address"}), 400
    if User.query.filter(or_(User.username == username, User.email == email)).first():
        return jsonify({"error": "username or email already exists"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    identity = (data.get("identity") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter(
        or_(User.username == identity, User.email == identity.lower())
    ).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username/email or password"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }), 200
