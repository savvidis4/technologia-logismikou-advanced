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

class HomeService:
    """
    Business Logic Layer για τη σελίδα Home.
    Εδώ αποθηκεύονται και διαχειρίζονται τα δεδομένα του χρήστη
    (χωρίς masking ή formatting, γιατί αυτά γίνονται στο UI).
    """

    def __init__(self, balance=0.0, iban="", card_number=""):
        self._balance = balance
        self._iban = iban
        self._card_number = card_number

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
            "balance": self._balance,
            "iban": self._iban,
            "card_number": self._card_number
        }

    # =========================================================
    # STRING REPRESENTATION (για debugging)
    # =========================================================
    def __repr__(self):
        return f"<HomeService balance={self._balance} iban='{self._iban}' card='****{self._card_number[-4:]}' />"
