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

    @classmethod
    def create_account(cls, user_id, iban, card_number, euro_balance=0.0, usd_balance=0.0, gbp_balance=0.0, yen_balance=0.0):

        new_account = cls(
            user_id=user_id,
            iban=iban,
            card_number=card_number,
            euro_balance=euro_balance,
            usd_balance=usd_balance,
            gbp_balance=gbp_balance,
            yen_balance=yen_balance
        )

        db.session.add(new_account)
        db.session.commit()

        return new_account
    
    @classmethod
    def add_funds(cls, iban, amount, currency):

        account = db.session.query(cls).filter_by(iban=iban).first()
        
        if not account:
            return False

        if currency == "EUR":
            account.euro_balance += amount
        elif currency == "USD":
            account.usd_balance += amount
        elif currency == "GBP":
            account.gbp_balance += amount
        elif currency == "JPY":
            account.yen_balance += amount

        db.session.commit()
        return True
    
    @classmethod
    def deduct_funds(cls, iban, amount, currency, added):

        account = db.session.query(cls).filter_by(iban=iban).first()
        
        if not account or not added:
            return False

        if currency == "EUR":
            account.euro_balance -= amount
        elif currency == "USD":
            account.usd_balance -= amount
        elif currency == "GBP":
            account.gbp_balance -= amount
        elif currency == "JPY":
            account.yen_balance -= amount

        db.session.commit()
        return True
        
