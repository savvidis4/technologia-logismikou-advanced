import random
from datetime import datetime
import re
from app.models import User, Account, Card

class AccountCreationService:

    """Business Logic για δημιουργία χρήστη και τραπεζικού λογαριασμού."""

    def __init__(self, db_session):

        #Dependency Injection — παίρνει session της βάσης.
        self.db = db_session

    #Δημιουργεί τυχαίο IBAN τύπου GR + [20 random digits] + user_id suffix
    def iban_generator(self):

        iban = 'GR'
        number = random.randint(100000000000000000000,999999999999999999999)
        last = self.db.query(User).count() + 1
        if len(str(last)) != 4:
            i = 4 - len(str(last))
            rlast = i * '0' + str(last)
        iban += str(number) + str(rlast)
        return iban 

    def card_generator(self):
    
        f = []
        card_number = '5175'
        number = random.randint(10000000,99999999)
        last = self.db.query(User).count() + 1
        if len(str(last)) != 4:
            i = 4 - len(str(last))
            rlast = i * '0' + str(last)

        card_number += str(number) + str(rlast)

        card_exp = str(datetime.date(datetime.now()))[5:7] + '/' + str(int(str(datetime.date(datetime.now()))[2:4]) + 5)

        cvv = random.randint(100,999)

        return {
            "card_number": card_number,
            "card_exp": card_exp,
            "card_cvv": cvv
        }

    def validate_data(self, email, password, confirm_password):

        if not email or not password or not confirm_password:
            return {"success": False, "message": "All fields are required."}

        # Έλεγχος αν υπάρχει ήδη χρήστης με το ίδιο email
        if self.db.query(User).filter_by(email=email).first():
            return {"success": False, "message": "Email already in use."}

        # ---------------- Email format check ----------------
        if not self.is_valid_email(email):
            return {"success": False, "message": "Email not valid."}

        # ---------------- Password strength check ----------------
        if password != confirm_password:
            return {"success": False, "message": "Passwords do not match."}

        if len(password) < 8:
            return {
                "success": False,
                "message": "Password needs to contain at least 8 characters."
            }
        
        has_upper = any(ch.isupper() for ch in password)
        has_num = any(ch.isdigit() for ch in password)
        has_symbol = any(ch in ['!', '@', '?', '#', '$', '%', '*'] for ch in password)

        if not (has_upper and has_num and has_symbol):
            return {
                "success": False,
                "message": "Password needs to contain a capital letter, a number and a symbol (!,@,?,#,...)"
                
            }
        
        return {"success": True, "message": "Validation passed."}
        
    @staticmethod
    def is_valid_email(email):
        pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return re.match(pattern, email) is not None
    

    # ACCOUNT CREATION (business logic)
    def create_account(self, email, password, confirm_password):

        """
        Δημιουργεί νέο χρήστη και τραπεζικό λογαριασμό μετά από ελέγχους.
        Επιστρέφει dict (success, message).
        """

        check = self.validate_data(email, password, confirm_password)

        if not check["success"]:
            return check

        try:

            # Δημιουργία IBAN και κάρτας
            iban = self.iban_generator()
            card = self.card_generator()

            # Δημιουργία νέου χρήστη
            new_user = User.create_user(email, password)

            new_account = Account.create_account(user_id=new_user.id, iban=iban, card_number=card["card_number"], euro_balance=0.0)

            Card.create_card(account_id= new_account.id, card_number=card["card_number"], card_exp_date=card["card_exp"], card_cvv=str(card["card_cvv"]), card_pin=str(card["card_number"][-4:]))
            
            return {
                "success": True,
                "message": "Account created successfully.",
                "iban": iban,
                "card_number": card["card_number"],
                "card_exp": card["card_exp"],
                "card_cvv": card["card_cvv"]
            }
        
        except Exception as e:
            self.db.rollback()
            print("Error during account creation. ", e)
            return {"success": False, "message": "A problem occured. Please try again in a moment."}

   
    
