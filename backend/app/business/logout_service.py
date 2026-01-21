from app.models import User
from flask_jwt_extended import create_access_token
from flask import jsonify

class LogoutService:

    def __init__(self, db_session):

        self.db = db_session
        
    def logout(self):
        return jsonify({"success": True, "message": "Logged out successfully."}), 200