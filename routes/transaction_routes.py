from flask import Blueprint, request, jsonify
from services.auth_service import authenticate
from database import transfer_money, get_transactions
from datetime import datetime, timedelta

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    token = data.get("token")
    receiver = data.get("receiver")
    amount = data.get("amount")

    sender = authenticate(token)
    if not sender:
        return jsonify({"error": "Invalid session"}), 401

    if not receiver or amount is None or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    result = transfer_money(sender, receiver, amount)

    if result == "Success":
        return jsonify({"message": "Transfer successful"})
    return jsonify({"error": result}), 400


@transaction_bp.route("/transactions", methods=["POST"])
def transactions():
    data = request.get_json()
    token = data.get("token")

    username = authenticate(token)
    if not username:
        return jsonify({"error": "Invalid session"}), 401

    records = get_transactions(username)

    result = []

    for r in records:
    # convert UTC to IST (+5:30)
        utc_time = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
        ist_time = utc_time + timedelta(hours=5, minutes=30)

        result.append({
            "from": r["sender"],
            "to": r["receiver"],
            "amount": r["amount"],
            "time": ist_time.strftime("%Y-%m-%d %I:%M:%S %p")
        })

    return jsonify(result)