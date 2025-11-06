# app/business/account_creation_service.py

"""
=============================================================
 Business Logic Layer - Account Creation
=============================================================
Καθαρή υλοποίηση της λειτουργικότητας εγγραφής χρήστη,
χωρίς UI, χωρίς messagebox, χωρίς tkinter.

Εφαρμόζει dependency injection (δέχεται db_session απ' έξω),
και περιλαμβάνει:

 - iban_generator()
 - card_generator()
 - account_creation() (εγγραφή χρήστη με ελέγχους)
"""

import random
import datetime
import re
from app.models import User, Account


class AccountCreationService:
    """Business Logic για δημιουργία χρήστη και τραπεζικού λογαριασμού."""

    def __init__(self, db_session):

        """
        Dependency Injection — παίρνει session της βάσης.
        """

        self.db = db_session

    # =========================================================
    # IBAN GENERATOR
    # =========================================================
    def _iban_generator(self):
        """
        Δημιουργεί τυχαίο IBAN τύπου GR + [20 random digits] + user_id suffix
        """
        iban = "GR"
        number = random.randint(100000000000000000000, 999999999999999999999)
        user_count = self.db.query(User).count() + 1
        suffix = str(user_count).zfill(4)
        iban += str(number) + suffix
        return iban

    # =========================================================
    # CARD GENERATOR
    # =========================================================
    def _card_generator(self):
        """
        Δημιουργεί αριθμό κάρτας, ημερομηνία λήξης και CVV.
        Επιστρέφει dict: {"card_number": ..., "exp": ..., "cvv": ...}
        """
        prefix = "5175"
        number = random.randint(10000000, 99999999)
        user_count = self.db.query(User).count() + 1
        suffix = str(user_count).zfill(4)

        card_number = prefix + str(number) + suffix
        now = datetime.datetime.now()
        exp_month = now.strftime("%m")
        exp_year = str(int(now.strftime("%y")) + 5)
        exp_date = f"{exp_month}/{exp_year}"
        cvv = random.randint(100, 999)

        return {
            "card_number": card_number,
            "card_exp": exp_date,
            "card_cvv": cvv
        }

    # =========================================================
    # ACCOUNT CREATION (business logic)
    # =========================================================
    def create_account(self, email, password, confirm_password):
        """
        Δημιουργεί νέο χρήστη και τραπεζικό λογαριασμό μετά από ελέγχους.
        Επιστρέφει dict (success, message).
        """

        # Έλεγχος αν υπάρχει ήδη χρήστης με το ίδιο email
        if self.db.query(User).filter_by(email=email).first():
            return {"success": False, "message": "Το email χρησιμοποιείται ήδη."}

        # ---------------- Email format check ----------------
        if not self._is_valid_email(email):
            return {"success": False, "message": "Μη έγκυρη διεύθυνση email."}

        # ---------------- Password strength check ----------------
        if password != confirm_password:
            return {"success": False, "message": "Οι κωδικοί δεν ταιριάζουν."}

        if len(password) < 8:
            return {
                "success": False,
                "message": "Ο κωδικός πρέπει να έχει τουλάχιστον 8 χαρακτήρες."
            }

        has_upper = any(ch.isupper() for ch in password)
        has_num = any(ch.isdigit() for ch in password)
        has_symbol = any(ch in ['!', '@', '?', '#', '$', '%', '*'] for ch in password)

        if not (has_upper and has_num and has_symbol):
            return {
                "success": False,
                "message": (
                    "Ο κωδικός πρέπει να περιέχει κεφαλαίο γράμμα, "
                    "αριθμό και ειδικό σύμβολο (!,@,?,#,...)"
                )
            }

        # ---------------- Account Generation ----------------
        try:
            # Δημιουργία νέου χρήστη
            new_user = User(
                username=email,       # μπορούμε να χρησιμοποιήσουμε το email ως username
                email=email,
                password=password
            )
            self.db.add(new_user)
            self.db.flush()  # παίρνουμε το user.id πριν το commit

            # Δημιουργία IBAN και κάρτας
            iban = self._iban_generator()
            card = self._card_generator()

            # Δημιουργία τραπεζικού λογαριασμού
            new_account = Account(
                user_id=new_user.id,
                euro_balance=0.0,
                iban=iban,
                card_number=card["card_number"]
            )
            self.db.add(new_account)
            self.db.commit()

            return {
                "success": True,
                "message": "Ο λογαριασμός δημιουργήθηκε επιτυχώς.",
                "iban": iban,
                "card_number": card["card_number"],
                "card_exp": card["card_exp"],
                "card_cvv": card["card_cvv"]
            }
        except Exception:
            self.db.rollback()
            return {"success": False, "message": "Απρόσμενο σφάλμα κατά τη δημιουργία."}

    # =========================================================
    # EMAIL VALIDATION
    # =========================================================
    @staticmethod
    def _is_valid_email(email):
        pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return re.match(pattern, email) is not None
