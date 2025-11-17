from .home_route import home_bp
from .login_route import login_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)