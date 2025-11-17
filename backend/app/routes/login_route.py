from flask import Blueprint, request
from app.extensions import db
from app.business.login_service import LoginService

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    login_service = LoginService(db.session, email, password)

    return login_service.verify_credentials()