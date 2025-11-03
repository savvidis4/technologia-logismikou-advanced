from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Account
from app.extensions import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
@jwt_required()
def home_data():
    
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    account = Account.query.filter_by(user_id=current_user_id).first()

    if not user or not account:
        return jsonify({"error": "User not found"}), 404

    masked_card_number = "**** **** **** " + account.card_number[-4:]

    data = {
        "username": user.username,
        "email": user.email,
        "euro_balance": account.euro_balance,
        "iban": account.iban,
        "card_number": masked_card_number,
        "success": True
    }

    return jsonify(data)
