from flask import Blueprint, request, jsonify
from app.models import User, Account
from app.extensions import db
from flask_jwt_extended import create_access_token
import random

auth_bp = Blueprint('auth', __name__)

# 📘 Εγγραφή (register)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Δημιουργία νέου χρήστη
    user = User(username=username, email=email)
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


# 🔐 Σύνδεση (login)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Δημιουργία JWT token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token, "username": user.username, "success":True}), 200
