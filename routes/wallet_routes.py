from flask import Blueprint, request, jsonify
from services.auth_service import authenticate
from database import get_balance, update_balance

wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.route("/balance", methods=["POST"])
def balance():
    data = request.get_json()
    token = data.get("token")

    username = authenticate(token)
    if not username:
        return jsonify({"error": "Invalid session"}), 401

    return jsonify({"balance": get_balance(username)})


@wallet_bp.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    token = data.get("token")
    amount = data.get("amount")

    username = authenticate(token)
    if not username:
        return jsonify({"error": "Invalid session"}), 401

    if amount is None or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    update_balance(username, amount)
    return jsonify({"message": "Deposit successful", "new_balance": get_balance(username)})