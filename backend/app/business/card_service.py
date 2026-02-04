from app.models import User, Account, Card

class CardService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.card_number = None
        self.frozen = False
        self.exp_date = None
        self.cvv = None

        self.load_user_card_data(current_user_id)


    def load_user_card_data(self, current_user_id):

        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()
        card = self.db.query(Card).filter_by(card_number=account.card_number).first()

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία
        
        self.card_number = account.card_number
        self.frozen = card.frozen_card
        self.exp_date = card.card_exp_date
        self.cvv = card.card_cvv
    

    def toggle_card_freeze(self):

        card = self.db.query(Card).filter_by(card_number=self.card_number).first()

        Card.set_card_frozen(self.card_number)
        self.frozen = card.frozen_card

    # Επιστροφή σε dict
    def to_dict(self):

        return {
            
            "number": self.card_number,
            "isFrozen": self.frozen,
            "exp": self.exp_date,
            "cvv": self.cvv,
            "success": True
        }