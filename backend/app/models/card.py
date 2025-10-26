from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_exp_date = db.Column(db.String(5), nullable=False)  # Format: MM/YY
    card_cvv = db.Column(db.String(3), nullable=False)
    card_pin_hash = db.Column(db.String(255), nullable=False)
    frozen_card = db.Column(db.Boolean, default=False)

    def set_card_pin(self, pin):
        self.card_pin_hash = generate_password_hash(pin)
    
    def check_card_pin(self, pin):
        return check_password_hash(self.card_pin_hash, pin)