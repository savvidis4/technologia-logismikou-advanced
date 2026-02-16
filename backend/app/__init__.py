# from flask import Flask
# from flask_cors import CORS
# from config import Config
# from .extensions import db, jwt
# from .routes import register_routes

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # CORS για να συνδέεται το Vue frontend
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     # Initialize extensions (Dependency Injection)
#     db.init_app(app)
#     jwt.init_app(app)

#     # Register blueprints
#     register_routes(app)

#     return app

from flask import Flask
from flask_cors import CORS
from config import Config
from .extensions import db, jwt
from .routes import register_routes

# UPDATE: Accept an optional test_config argument
def create_app(test_config=None):
    app = Flask(__name__)

    # LOGIC CHANGE:
    # If a test_config is passed, use it!
    # Otherwise, load the normal Config (your real DB).
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    # CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    register_routes(app)

    return app
