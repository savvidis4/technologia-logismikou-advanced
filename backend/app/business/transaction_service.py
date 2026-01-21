from app.models import User, Account, Transactions

class TransactionService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.transaction_list = []
        
        self.load_transaction_data(current_user_id)

    def load_transaction_data(self, current_user_id):

        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()
        trans = self.db.query(Transactions).filter_by(account_id=account.id).all()

        

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία
        
        self.email = user.email
        self.balance = account.euro_balance
        self.iban = account.iban
        self.masked_card_number = "**** **** **** " + account.card_number[-4:]

    # Επιστροφή σε dict
    def to_dict(self):

        return {
            
            "balance": self.balance,
            "iban": self.iban,
            "card_number": self.masked_card_number,
            "email": self.email,
            "success": True
        }
