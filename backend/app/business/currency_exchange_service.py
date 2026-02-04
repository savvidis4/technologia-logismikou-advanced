from app.models import User, Account, Transactions
from flask import jsonify

class CurrencyExchangeService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.euro_balance = None
        self.usd_balance = None
        self.gbp_balance = None
        self.yen_balance = None
        self.errmsg = None

        self.load_user_data(current_user_id)


    def load_user_data(self, current_user_id):

        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία
        self.euro_balance = account.euro_balance
        self.usd_balance = account.usd_balance
        self.gbp_balance = account.gbp_balance
        self.yen_balance = account.yen_balance

    
    def convert_currency(self, current_user_id, from_currency, to_currency, amount):
        # Υλοποίηση λογικής μετατροπής νομισμάτων
        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")
        
        if from_currency == to_currency:
            self.errmsg = "From and To currencies cannot be the same."
            return 0.0

        
        if from_currency not in ["EUR", "USD", "GBP", "JPY"] or to_currency not in ["EUR", "USD", "GBP", "JPY"]:
            self.errmsg = "Invalid currency code."
            return 0.0
        
        if amount <= 0:
            self.errmsg = "Amount must be greater than zero."
            return 0.0
        
        if from_currency == "EUR" and account.euro_balance < amount:
            self.errmsg = "Insufficient EUR balance."
            return 0.0
        elif from_currency == "USD" and account.usd_balance < amount:
            self.errmsg = "Insufficient USD balance."
            return 0.0
        elif from_currency == "GBP" and account.gbp_balance < amount:
            self.errmsg = "Insufficient GBP balance."
            return 0.0
        elif from_currency == "JPY" and account.yen_balance < amount:
            self.errmsg = "Insufficient JPY balance."
            return 0.0

        converted_amount = Account.convert_currency(account.iban, from_currency, to_currency, amount)

        Transactions.create_transaction(
            account_id=account.id,
            iban_from=account.iban,
            iban_to=account.iban,
            amount="-" + str(amount),
            currency=from_currency,
            description="DEBIT"
        )

        Transactions.create_transaction(
            account_id=account.id,
            iban_from=account.iban,
            iban_to=account.iban,
            amount="+" + str(converted_amount),
            currency=to_currency,
            description="CREDIT"
        )

        return converted_amount

    # Επιστροφή σε dict
    def to_dict(self):

        return {
            "errmsg": self.errmsg,
            "converted_amount": 0.0,
            "euro_balance": self.euro_balance,
            "usd_balance": self.usd_balance,
            "gbp_balance": self.gbp_balance,
            "yen_balance": self.yen_balance,
            "success": True
        }