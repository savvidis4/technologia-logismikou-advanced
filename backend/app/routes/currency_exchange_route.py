from flask import Blueprint
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.business.currency_exchange_service import CurrencyExchangeService

currency_exchange_bp = Blueprint('currency_exchange', __name__)

@currency_exchange_bp.route('/exchange', methods=['GET', 'POST'])
@jwt_required()
def currency_exchange():

    current_user_id = int(get_jwt_identity())

    currency_exchange_service = CurrencyExchangeService(db.session, current_user_id)
    
    if flask.request.method == 'GET':

        data = currency_exchange_service.to_dict()

    elif flask.request.method == 'POST':

        converted_amount = currency_exchange_service.convert_currency(current_user_id, 
                                                  flask.request.json.get('currencyFrom'), 
                                                  flask.request.json.get('currencyTo'), 
                                                  flask.request.json.get('amount'))
        data = currency_exchange_service.to_dict()
        
        data["converted_amount"] = converted_amount

    return data