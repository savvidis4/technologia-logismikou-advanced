from app.extensions import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iban = db.Column(db.String(34), unique=True, nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
