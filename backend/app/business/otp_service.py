import random
from datetime import datetime
import re
from app.models import User, Account, Card

class OtpService:

    def __init__(self, db_session, current_user_id):

        #Dependency Injection — παίρνει session της βάσης.
        self.db = db_session
        self.otp = None
        self.user = None
        self.account = None

        self.find_data(current_user_id)

    def find_data(self, current_user_id):
        self.user = self.db.query(User).filter_by(id=current_user_id).first()
        self.account = self.db.query(Account).filter_by(user_id=current_user_id).first()
        self.otp = self.account.otp_secret


    def generate_otp(self):

        if not self.user:
            return ({"success": False, "message": "User not found."})

        if not self.account:
            return {"success": False, "message": "Account not found."}

        otp = self.account.generate_new_otp_secret()

        self.find_data(self.user.id)

        return {"success": True, "message": "OTP generated successfully.", "otp": otp}


    def verify_otp(self, current_user_id, otp):

        if not current_user_id or not otp:
            return {"success": False, "message": "All fields are required."}

        if not self.user:
            return {"success": False, "message": "User not found."}

        if not self.account:
            return {"success": False, "message": "Account not found."}

        if not self.account.check_otp_secret(otp):
            return {"success": False, "message": "Invalid OTP."}

        return {"success": True, "message": "OTP verified successfully."}