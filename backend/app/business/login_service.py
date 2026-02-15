from app.models import User, Account
from flask_jwt_extended import create_access_token
from flask import jsonify
from app.business.email_service import EmailService
from datetime import datetime

class LoginService:

    #Constructor με dependency injection.
    def __init__(self, db_session, email, password):

        self.db = db_session
        self.email = email
        self.password = password
        self.access_token = None
    
    
    def verify_credentials(self):

        # Αναζήτηση χρήστη
        user = self.db.query(User).filter_by(email=self.email).first()

        # Αν δεν βρεθεί ο χρήστης
        if not user or not user.check_password(self.password):
            return jsonify({"error": "Invalid email or password"}), 401

        self.access_token = create_access_token(identity=str(user.id))
        
        date = datetime.now()
        account = self.db.query(Account).filter_by(user_id=user.id).first()
        sender_email_service = EmailService()
        sender_email_service.set_email_data(user.email, "UniWAlerts Service", f'We would like to inform you that on {date} a login attempt was made on your account {account.iban}\n\nYours sinserely,\nUniWA Bank', False, False)
        sender_email_service.send_email()

        # Αν όλα είναι εντάξει δημιουργούμε json λίστα με τα στοιχεία του χρήστη
        return jsonify({
            "token": self.access_token,
            "success": True,
            "email": user.email,
            }), 200
        