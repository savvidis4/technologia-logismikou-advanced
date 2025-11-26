from app.models import User, Account

"""
=============================================================
 Business Logic Layer - Home Screen
=============================================================
Αυτό το αρχείο περιέχει την κλάση HomeService, η οποία λειτουργεί
ως μεσάζων μεταξύ του backend (βάση δεδομένων) και του frontend (Vue.js).

Σκοπός:
--------
Να επεξεργάζεται και να μορφοποιεί τα δεδομένα που αφορούν
την αρχική οθόνη e-Banking (balance, IBAN, card number),
ώστε να σταλούν έτοιμα προς εμφάνιση στο χρήστη.

Η HomeService:
  - Δέχεται δεδομένα από τη βάση (μέσω dependency injection)
  - Κάνει βασική επεξεργασία (format, masking)
  - Τα επιστρέφει στο Controller μέσω to_dict()
"""

class HomeService:

    #Constructor με dependency injection.
    def __init__(self, db_session, current_user_id):

        self.db = db_session
        self.balance = None
        self.iban = None
        self.card_number = None
        self.email = None

        self.load_user_data(current_user_id)

    def load_user_data(self, current_user_id):

        user = self.db.query(User).get(current_user_id)
        account = self.db.query(Account).filter_by(user_id=current_user_id).first()

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία
        self.username = user.username
        self.email = user.email
        self.balance = account.euro_balance
        self.iban = account.iban
        self.masked_card_number = "**** **** **** " + account.card_number[-4:]

    # Επιστροφή σε dict
    def to_dict(self):

        return {
            "username": self.username,
            "balance": self.balance,
            "iban": self.iban,
            "card_number": self.masked_card_number,
            "email": self.email,
            "success": True
        }
