from flask import Flask
from .config import Config
from .extensions import db, bcrypt, jwt, migrate
from flask_cors import CORS
from .routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    register_blueprints(app)

    return app
