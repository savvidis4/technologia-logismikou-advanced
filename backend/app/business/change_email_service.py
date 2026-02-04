import random
from datetime import datetime
import re
from app.models import User, Account, Card
from app.business.otp_service import OtpService

class ChangeEmailService:

    def __init__(self, db_session):

        self.db = db_session

    def email_change(self, current_user_id, old_email, new_email, ver_new_email):

        user = self.db.query(User).filter_by(id=current_user_id).first()

        if not current_user_id or not old_email or not new_email or not ver_new_email:
            return {"success": False, "message": "All fields are required."}

        if not user:
            return {"success": False, "message": "User not found."}

        if new_email != ver_new_email:
            return {"success": False, "message": "New emails do not match."}
        
        user.set_email(new_email)
        self.db.commit()

        return {"success": True, "message": "Email changed successfully."}