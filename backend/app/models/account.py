from app.extensions import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iban = db.Column(db.String(34), unique=True, nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    euro_balance = db.Column(db.Numeric(7,2), default=0.0)
    usd_balance = db.Column(db.Numeric(7,2), default=0.0)
    gbp_balance = db.Column(db.Numeric(7,2), default=0.0)
    yen_balance = db.Column(db.Numeric(7,2), default=0.0)
    otp_secret = db.Column(db.String(6), nullable=True)

