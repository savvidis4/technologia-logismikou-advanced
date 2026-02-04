import random
from datetime import datetime
import re
from app.models import User, Account, Card

class ChangePasswordService:

    """Business Logic για αλλαγή password."""

    def __init__(self, db_session, current_user_id):

        #Dependency Injection — παίρνει session της βάσης.
        self.db = db_session
        self.user = None

        self.find_data(current_user_id)

    def find_data(self, current_user_id):
        self.user = self.db.query(User).filter_by(id=current_user_id).first()

    def password_change(self, current_user_id, old_password, new_password, ver_new_password):

        if not current_user_id or not old_password or not new_password or not ver_new_password:
            return {"success": False, "message": "All fields are required."}

        if not self.user:
            return {"success": False, "message": "User not found."}

        if not self.user.check_password(old_password):
            return {"success": False, "message": "Old password is incorrect."}

        if new_password != ver_new_password:
            return {"success": False, "message": "New passwords do not match."}

        self.user.set_password(new_password)
        self.db.commit()

        return {"success": True, "message": "Password changed successfully!"}