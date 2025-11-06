# app/business/home_service.py

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
  - Δέχεται δεδομένα από τη βάση (μέσω άλλης υπηρεσίας ή API call)
  - Τα αποθηκεύει σε ιδιωτικά πεδία (με setters/getters)
  - Κάνει βασική επεξεργασία (format, masking)
  - Τα επιστρέφει στο Controller μέσω to_dict()
"""

from app.models import User, Account

class HomeService:
    """
    Business Logic Layer για τη σελίδα Home.
    Εδώ αποθηκεύονται και διαχειρίζονται τα δεδομένα του χρήστη
    (χωρίς masking ή formatting, γιατί αυτά γίνονται στο UI).
    """

    def __init__(self, db_session, current_user_id):

        """Constructor με dependency injection."""""

        self.db = db_session
        self._username = None
        self._balance = None
        self._iban = None
        self._card_number = None
        self._email = None

        # Έλεγχος δεδομένων χρήστη
        self._load_user_data(current_user_id)


    def _load_user_data(self, current_user_id):
        """
        Ελέγχει αν υπάρχει ο χρήστης και ο λογαριασμός.
        Αν βρεθούν, φορτώνει τα δεδομένα στο αντικείμενο.
        """

        user = User.query.get(current_user_id)
        account = Account.query.filter_by(user_id=current_user_id).first()

        if not user or not account:
            # Δεν επιστρέφουμε jsonify εδώ (το κάνει ο controller)
            raise ValueError("User not found")

        # Αποθήκευση δεδομένων στα private πεδία
        self._username = user.username
        self._email = user.email
        self._balance = account.euro_balance
        self._iban = account.iban
        self._card_number = account.card_number


    # Getters
    def get_balance(self):
        return self._balance

    def get_iban(self):
        return self._iban

    def get_card_number(self):
        return self._card_number

    # Επιστροφή σε dict (π.χ. για API απάντηση)
    def to_dict(self):
        return {
            "username": self._username,
            "euro_balance": self._balance,
            "iban": self._iban,
            "card_number": self._card_number,
            "email": self._email,
            "success": True

        }

    # =========================================================
    # STRING REPRESENTATION (για debugging)
    # =========================================================
    def __repr__(self):
        return f"<HomeService balance={self._balance} iban='{self._iban}' card='****{self._card_number[-4:]}' />"
