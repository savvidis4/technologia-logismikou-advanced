from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.business.transactions_service import TransactionsService

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    
    current_user_id = int(get_jwt_identity())

    transactions_service = TransactionsService(db.session, current_user_id)

    data = {"success": True, "transactions": transactions_service.transactions_list}

    return jsonify(data)