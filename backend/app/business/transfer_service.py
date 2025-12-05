from app.models import Account
from flask import jsonify

class TransferService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.account_iban = None
        self.currency_symbol = ""

        self.load_transfer_data(current_user_id)

    def load_transfer_data(self, current_user_id):

        account = self.db.query(Account).filter_by(user_id=current_user_id).first()

        if not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("Account not found")

        # Αποθήκευση δεδομένων στα private πεδία
        
        self.account_iban = account.iban

    def check_funds(self, amount, currency):
        # Απλή μέθοδος ελέγχου υπολοίπου
        account = self.db.query(Account).filter_by(iban=self.account_iban).first()
        if currency == "EUR":
            self.currency_symbol = "€ (EUR)"
            return account.euro_balance >= amount
        elif currency == "USD":
            self.currency_symbol = "$ (USD)"
            return account.usd_balance >= amount
        elif currency == "GBP":
            self.currency_symbol = "£ (GBP)"
            return account.gbp_balance >= amount
        elif currency == "JPY":
            self.currency_symbol = "¥ (JPY)"
            return account.jpy_balance >= amount
        else:
            return False
   
    def initiate_transfer(self, amount, currency, recipient_iban):

        print("Initiating transfer:", amount, currency, recipient_iban)
        if not self.check_funds(amount, currency):
            print(amount, currency, recipient_iban)
            return jsonify({"success": False, "message": "Insufficient funds."}), 401

        added = Account.add_funds(recipient_iban, amount, currency)
        Account.deduct_funds(self.account_iban, amount, currency, added)

        return jsonify({"success": True, "message": f"Transfer of {amount} {self.currency_symbol} to account with IBAN {recipient_iban} was successfull."}), 200
    
    def to_dict(self):

        return jsonify({
            
            "account_iban": self.account_iban,
            "success": True
        }), 200
