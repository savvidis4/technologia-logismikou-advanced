from app.models import User, Account, Transactions

        

class TransactionsService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.id = None
        self.iban_from = None
        self.iban_to = None
        self.amount = None
        self.cur = None
        self.date = None
        self.description = None

        self.transactions_list = self.load_transaction_data(current_user_id)

    def load_transaction_data(self, current_user_id):

        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()
        trans = self.db.query(Transactions).filter_by(account_id=account.id).all()
        
        transaction_list = []

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία

        for t in trans:
            
            self.id = t.id
            self.iban_from = t.iban_from
            self.iban_to = t.iban_to
            self.amount = t.amount
            self.cur = t.currency
            self.date = t.trans_date
            self.description = t.description
            transaction_list.append([self.id, self.iban_from, self.iban_to, self.amount, self.cur, self.date, self.description])
        
        return transaction_list

    @classmethod
    def get_transactions_list(cls, db_session, current_user_id):
        service = cls(db_session, current_user_id)
        return service.transactions_list

    # # Επιστροφή σε dict
    # def to_dict(self):

    #     return {
            
    #         "balance": self.balance,
    #         "iban": self.iban,
    #         "card_number": self.masked_card_number,
    #         "email": self.email,
    #         "success": True
    #     }
