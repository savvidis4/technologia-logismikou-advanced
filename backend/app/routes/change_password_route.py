from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.business.change_password_service import ChangePasswordService
 
change_password_bp = Blueprint('change_password', __name__)

@change_password_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():

    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    old = data.get('old_password')
    new_password = data.get('new_password')
    new_ver_password = data.get('new_password_verification')

    change_password_service = ChangePasswordService(db.session, current_user_id)

    result = change_password_service.password_change(current_user_id, old, new_password, new_ver_password)

    return jsonify(result)