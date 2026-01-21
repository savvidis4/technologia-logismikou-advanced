from .home_route import home_bp
from .login_route import login_bp
from .register_route import register_bp
from .transfer_route import transfer_bp
from .card_route import card_bp
from .transactions_route import transactions_bp
from .currency_exchange_route import currency_exchange_bp
from .logout_route import logout_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(transfer_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(currency_exchange_bp)
    app.register_blueprint(logout_bp)
