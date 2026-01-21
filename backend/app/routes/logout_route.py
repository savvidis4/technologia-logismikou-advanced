from flask import Blueprint, request
from app.extensions import db
from app.business.logout_service import LogoutService

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['POST'])
def logout():

    logout_service = LogoutService(db.session)

    return logout_service.logout()