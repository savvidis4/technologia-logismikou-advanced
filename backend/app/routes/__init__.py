from .home_route import home_bp
from .login_route import login_bp
from .register_route import register_bp
from .transfer_route import transfer_bp
from .card_route import card_bp
from .transactions_route import transactions_bp
from .currency_exchange_route import currency_exchange_bp
from .logout_route import logout_bp
from .graphs_route import graphs_bp
from .change_pin_route import change_pin_bp
from .otp_route import otp_bp
from .change_password_route import change_password_bp
from .change_email_route import change_email_bp
from .forgot_password_route import forgot_password_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(currency_exchange_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(graphs_bp)
    app.register_blueprint(change_pin_bp)
    app.register_blueprint(otp_bp)
    app.register_blueprint(change_password_bp)
    app.register_blueprint(change_email_bp)
    app.register_blueprint(forgot_password_bp)


