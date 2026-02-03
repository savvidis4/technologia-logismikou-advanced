import decimal
import random
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

    @staticmethod
    def calcValue(amount, cur_from, cur_to):
        rates = {
            "EUR": {"USD": 1.1703, "JPY": 185.1487, "GBP": 0.8716},
            "USD": {"EUR": 0.8543, "JPY": 158.1766, "GBP": 0.7446},
            "JPY": {"EUR": 0.0054, "USD": 0.0063, "GBP": 0.0047},
            "GBP": {"EUR": 1.1473, "USD": 1.3427, "JPY": 212.3886}
        }

        return float(amount) * rates[cur_from][cur_to]
    
    @classmethod
    def convert_currency(cls, iban, from_currency, to_currency, amount):

        account = db.session.query(cls).filter_by(iban=iban).first()
        converted_amount = 0.0
        if not account:
            return False

        if from_currency == "EUR" and to_currency == "USD":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.euro_balance -= amount
            account.usd_balance += decimal.Decimal(converted_amount)
        elif from_currency == "EUR" and to_currency == "GBP":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.euro_balance -= amount
            account.gbp_balance += decimal.Decimal(converted_amount)
        elif from_currency == "EUR" and to_currency == "JPY":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.euro_balance -= amount
            account.yen_balance += decimal.Decimal(converted_amount)
        elif from_currency == "USD" and to_currency == "GBP":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.usd_balance -= amount
            account.gbp_balance += decimal.Decimal(converted_amount)
        elif from_currency == "USD" and to_currency == "JPY":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.usd_balance -= amount
            account.yen_balance += decimal.Decimal(converted_amount)
        elif from_currency == "USD" and to_currency == "EUR":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.usd_balance -= amount
            account.euro_balance += decimal.Decimal(converted_amount)
        elif from_currency == "GBP" and to_currency == "JPY":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.gbp_balance -= amount
            account.yen_balance += decimal.Decimal(converted_amount)
        elif from_currency == "GBP" and to_currency == "USD":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.gbp_balance -= amount
            account.usd_balance += decimal.Decimal(converted_amount)
        elif from_currency == "GBP" and to_currency == "EUR":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.gbp_balance -= amount
            account.euro_balance += decimal.Decimal(converted_amount)
        elif from_currency == "JPY" and to_currency == "EUR":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.yen_balance -= amount
            account.euro_balance += decimal.Decimal(converted_amount)
        elif from_currency == "JPY" and to_currency == "USD":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.yen_balance -= amount
            account.usd_balance += decimal.Decimal(converted_amount)
        elif from_currency == "JPY" and to_currency == "GBP":
            converted_amount = Account.calcValue(amount, from_currency, to_currency)
            account.yen_balance -= amount
            account.gbp_balance += decimal.Decimal(converted_amount)

        db.session.commit()
        return converted_amount

    @classmethod
    def generate_new_otp_secret(self):
        self.otp_secret = str(random.randint(100000, 999999))
        db.session.commit()
        return self.otp_secret
    
    @classmethod
    def check_otp_secret(self, test_otp):
        return self.otp_secret == test_otp
    
    @classmethod
    def get_otp(self):
        return self.otp_secret