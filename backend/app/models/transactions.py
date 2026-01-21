from app.extensions import db

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    iban_from = db.Column(db.String(34), unique=True, nullable=False)
    iban_to = db.Column(db.String(34), unique=True, nullable=False)
    amount = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    trans_date = db.Column(db.DateTime, server_default=db.func.now())
    description = db.Column(db.String(255))
 