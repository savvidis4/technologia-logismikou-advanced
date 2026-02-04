from flask import Blueprint
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.business.card_service import CardService

card_bp = Blueprint('card', __name__)

@card_bp.route('/card', methods=['GET', 'POST'])
@jwt_required()
def card():
    
    current_user_id = int(get_jwt_identity())

    card_service = CardService(db.session, current_user_id)

    data = card_service.to_dict()

    if flask.request.method == 'POST':
        card_service.toggle_card_freeze()
        data = card_service.to_dict()

    return data