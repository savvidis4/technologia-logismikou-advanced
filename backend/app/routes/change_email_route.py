from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.business.change_email_service import ChangeEmailService
 
change_email_bp = Blueprint('change_email', __name__)

@change_email_bp.route('/change_email', methods=['POST'])
@jwt_required()
def change_email():

    # 1. Handle OPTIONS (Preflight)
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200

    current_user_id = int(get_jwt_identity())
    if not current_user_id:
        return jsonify({"success": False, "message": "User not authenticated."}), 401
    
    data = request.get_json()
    old = data.get('old_email')
    new_email = data.get('new_email')
    new_ver_email = data.get('new_email_verification')

    change_email_service = ChangeEmailService(db.session)

    result = change_email_service.email_change(current_user_id, old, new_email, new_ver_email)

    return jsonify(result)