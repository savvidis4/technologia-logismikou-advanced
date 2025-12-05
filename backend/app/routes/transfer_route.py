from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.business.transfer_service import TransferService

transfer_bp = Blueprint('transfers', __name__)

@transfer_bp.route('/transfers', methods=['GET', 'POST'])
@jwt_required()
def transfers():

    current_user_id = int(get_jwt_identity())
    transfer_service = TransferService(db.session, current_user_id)
    transfer_data = transfer_service.to_dict()

    if request.method == 'POST':

        data = request.get_json()
        amount = data.get('amount')
        currency = data.get('currency')
        recipient_iban = data.get('recipient')

        current_user_id = int(get_jwt_identity())

        result = transfer_service.initiate_transfer(amount, currency, recipient_iban)

        return result
    
    else:
    
        return transfer_data