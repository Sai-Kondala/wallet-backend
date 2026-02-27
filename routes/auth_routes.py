from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_user_by_username, get_connection
from services.auth_service import create_session, logout

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except:
        conn.close()
        return jsonify({"error": "Username already exists"}), 409


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username)

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_session(username)

    return jsonify({"message": "Login successful", "token": token})


@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    data = request.get_json()
    token = data.get("token")

    if logout(token):
        return jsonify({"message": "Logged out successfully"})
    return jsonify({"error": "Invalid session"}), 401