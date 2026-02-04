from app.extensions import db

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    iban_from = db.Column(db.String(34), nullable=False)
    iban_to = db.Column(db.String(34), nullable=False)
    amount = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    trans_date = db.Column(db.DateTime, server_default=db.func.now())
    description = db.Column(db.String(255))

    @classmethod
    def create_transaction(cls, account_id, iban_from, iban_to, amount, currency, description):
        new_transaction = cls(
            account_id=account_id,
            iban_from=iban_from,
            iban_to=iban_to,
            amount=amount,
            currency=currency,
            description=description
        )

        db.session.add(new_transaction)
        db.session.commit()
    
    
