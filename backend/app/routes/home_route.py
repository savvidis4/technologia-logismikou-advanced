from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Account
from app.extensions import db
from app.business.home_service import HomeService

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
@jwt_required()
def home_data():
    
    current_user_id = int(get_jwt_identity())

    home_service = HomeService(db.session, current_user_id)

    data = home_service.to_dict()

    return data
