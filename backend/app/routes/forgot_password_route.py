from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.business.forgot_password_service import ForgotPasswordService
 
forgot_password_bp = Blueprint('forgot_password', __name__)

@forgot_password_bp.route('/forgot_password', methods=['POST', 'GET'])
@jwt_required()
def forgot_password():

    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    return jsonify({"success": True, "message": "Continue"})
   
        


