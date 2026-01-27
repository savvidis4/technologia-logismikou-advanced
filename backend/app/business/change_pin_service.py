import random
from datetime import datetime
import re
from app.models import User, Account, Card

class ChangePinService:

    """Business Logic για αλλαγή PIN."""

    def __init__(self, db_session, current_user_id):

        #Dependency Injection — παίρνει session της βάσης.
        self.db = db_session
        self.user = None
        self.account = None
        self.card = None

        self.find_data(current_user_id)

    def find_data(self, current_user_id):
        self.user = self.db.query(User).filter_by(id=current_user_id).first()
        self.account = self.db.query(Account).filter_by(user_id=current_user_id).first()
        self.card = self.db.query(Card).filter_by(account_id=self.account.id).first()

    def pin_change(self, current_user_id, old_pin, new_pin, ver_new_pin):

        if not current_user_id or not old_pin or not new_pin or not ver_new_pin:
            return {"success": False, "message": "All fields are required."}

        if not self.user:
            return {"success": False, "message": "User not found."}

        if not self.card:
            return {"success": False, "message": "Card not found."}

        if not self.card.check_card_pin(old_pin):
            return {"success": False, "message": "Old PIN is incorrect."}

        if new_pin != ver_new_pin:
            return {"success": False, "message": "New PINs do not match."}

        self.card.set_card_pin(new_pin)
        self.db.commit()

        return {"success": True, "message": "PIN changed successfully."}
    