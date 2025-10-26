from flask import Flask
from flask_cors import CORS
from config import Config
from .extensions import db, jwt
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS για να συνδέεται το Vue frontend
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions (Dependency Injection)
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    register_routes(app)

    return app
