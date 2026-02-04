from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.business.change_pin_service import ChangePinService
 
change_pin_bp = Blueprint('change_pin', __name__)

@change_pin_bp.route('/change_pin', methods=['POST'])
@jwt_required()
def change_pin():

    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    old = data.get('old_pin')
    new_pin = data.get('new_pin')
    new_ver_pin = data.get('new_pin_verification')

    change_pin_service = ChangePinService(db.session, current_user_id)

    result = change_pin_service.pin_change(current_user_id, old, new_pin, new_ver_pin)

    return jsonify(result)


