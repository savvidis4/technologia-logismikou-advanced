from app.models import User
from flask_jwt_extended import create_access_token
from flask import jsonify

"""
=============================================================
 Business Logic Layer - Login 
=============================================================
Η κλάση LoginService είναι υπεύθυνη για τη λογική σύνδεσης χρηστών.

Δέχεται db_session μέσω dependency injection και ελέγχει αν το email
και ο κωδικός ταιριάζουν με αυτά της βάσης.
"""

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
        
        # Αν όλα είναι εντάξει δημιουργούμε json λίστα με τα στοιχεία του χρήστη
        return jsonify({
            "token": self.access_token,
            "success": True,
            "username": user.username,
            }), 200
        