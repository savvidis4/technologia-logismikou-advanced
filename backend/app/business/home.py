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
    """Κλάση Business Logic για τη σελίδα Home."""

    def __init__(self, balance=0.0, iban="", card_number=""):
        """
        Constructor: αρχικοποιεί τα δεδομένα της αρχικής σελίδας.

        :param balance: Υπόλοιπο του λογαριασμού (float)
        :param iban: IBAN του χρήστη (string)
        :param card_number: Αριθμός κάρτας (string)
        """
        self._balance = balance
        self._iban = iban
        self._card_number = card_number

    # =========================================================
    # GETTERS
    # =========================================================
    def get_balance(self):
        """Επιστρέφει το υπόλοιπο του χρήστη με 2 δεκαδικά."""
        return round(self._balance, 2)

    def get_iban(self):
        """Επιστρέφει το IBAN του χρήστη σε καθαρή μορφή."""
        return self._iban.strip()

    def get_card_number(self):
        """Επιστρέφει τον πλήρη αριθμό της κάρτας."""
        return self._card_number


    # =========================================================
    # SETTERS
    # =========================================================
    def set_balance(self, new_balance):
        """Αλλάζει το υπόλοιπο, μόνο αν είναι έγκυρος θετικός αριθμός."""
        if isinstance(new_balance, (int, float)) and new_balance >= 0:
            self._balance = new_balance
        else:
            raise ValueError("Το υπόλοιπο πρέπει να είναι θετικός αριθμός.")

    def set_iban(self, new_iban):
        """Αλλάζει το IBAN, εφόσον είναι string."""
        if isinstance(new_iban, str) and len(new_iban) >= 10:
            self._iban = new_iban
        else:
            raise ValueError("Το IBAN πρέπει να είναι συμβολοσειρά με έγκυρο μήκος.")

    def set_card_number(self, new_card):
        """Αλλάζει τον αριθμό κάρτας, εφόσον είναι string."""
        if isinstance(new_card, str) and len(new_card) >= 4:
            self._card_number = new_card
        else:
            raise ValueError("Ο αριθμός κάρτας πρέπει να είναι συμβολοσειρά τουλάχιστον 4 ψηφίων.")

    # =========================================================
    # BUSINESS LOGIC HELPERS
    # =========================================================
    def formatted_balance(self):
        """Επιστρέφει το υπόλοιπο μορφοποιημένο για εμφάνιση."""
        return f"{self.get_balance():,.2f} €"

    def short_iban(self):
        """Επιστρέφει συντομευμένο IBAN (π.χ. GR30...9002)."""
        iban = self.get_iban()
        if len(iban) > 8:
            return f"{iban[:6]}...{iban[-4:]}"
        return iban

    # =========================================================
    # EXPORT METHOD
    # =========================================================
    def to_dict(self):
        """
        Επιστρέφει τα δεδομένα σε μορφή λεξικού (dictionary),
        κατάλληλη για μετατροπή σε JSON στο Controller.
        """
        return {
            "balance": self.formatted_balance(),
            "iban": self.short_iban(),
            "card_number": self.get_card_number()
        }

    # =========================================================
    # STRING REPRESENTATION (για debugging)
    # =========================================================
    def __repr__(self):
        return f"<HomeService balance={self._balance} iban='{self._iban}' card='****{self._card_number[-4:]}' />"
