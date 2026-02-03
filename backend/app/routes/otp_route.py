from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.business.otp_service import OtpService
from app.business.email_service import EmailService
from app.models import User

otp_bp = Blueprint('otp', __name__)

@otp_bp.route('/otp', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required() 
def otp():
    # 1. Handle OPTIONS (Preflight)
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200

    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"success": False, "message": "User not authenticated."}), 401
    
    current_user_id = int(current_user_id)

    # 2. Handle GET (Send Email)
    if request.method == 'GET':
        # REMOVED: data = request.get_json()  <-- This was causing the 415 error!
        
        email_service = EmailService()
        user = db.session.query(User).filter_by(id=current_user_id).first()
        
        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404
        
        otp_service = OtpService(db.session, current_user_id)
        otp_result = otp_service.generate_otp()
        otp_code = otp_result["otp"]

        user_email = user.email
        message = f"Uniwa Bank account Security code \n\nPlease use the following security code to verify your account.\n\nSecurity code: {otp_code}\n\nOnly enter this code on an official app. Don't share it with anyone. We'll never ask for it outside an official platform.\n\nThanks,\n\nThe Uniwa Bank account team"

        theme = "Uniwa Bank account security code"

        email_service.set_email_data(user_email, theme, message, True, True)

        return email_service.send_email()
    
    # 3. Handle POST (Verify Code)
    elif request.method == 'POST':
        # MOVED HERE: Only try to read JSON if it is actually a POST request
        data = request.get_json() 
        
        if not data or 'otp_code' not in data:
             return jsonify({"success": False, "message": "Missing OTP code."}), 400

        otp_code = data.get('otp_code')
        otp_service = OtpService(db.session, otp_code)

        return otp_service.verify_otp(current_user_id, otp_code)