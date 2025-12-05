from .home_route import home_bp
from .login_route import login_bp
from .register_route import register_bp
from .transfer_route import transfer_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(transfer_bp)