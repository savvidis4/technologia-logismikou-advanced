from flask import Blueprint, request, jsonify
from app.extensions import db
from app.business.register_service import AccountCreationService
 
register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    ver_password = data.get('ver_password')

    register_service = AccountCreationService(db.session)

    new_user = register_service.create_account(email, password, ver_password)

    if new_user["success"] == False:
        print("Registration failed:", new_user["message"])
        return jsonify({"message": new_user["message"]}), 400

    return jsonify(new_user), 201



