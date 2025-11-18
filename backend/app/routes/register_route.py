from flask import Blueprint, request, jsonify
from app.models import User, Account
from app.extensions import db
from flask_jwt_extended import create_access_token
import random
 
register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    ver_password = data.get('ver_password')

    if not email or not password or not ver_password:
        return jsonify({"error": "Missing fields"}), 400
    
    if password != ver_password:
        return jsonify({"error": "Passwords do not match"}), 400
    
    if db.session.query(User).filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 400

    # Δημιουργία νέου χρήστη
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Δημιουργία λογαριασμού
    iban = f"GR{random.randint(10**25, 10**26 - 1)}"
    card_number = str(random.randint(4000000000000000, 4999999999999999))
    account = Account(user_id=user.id, iban=iban, card_number=card_number, euro_balance=50000)
    db.session.add(account)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



