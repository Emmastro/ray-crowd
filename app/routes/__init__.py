from flask import Flask

from .auth import auth_bp
from .proxy import proxy_bp
from .version import version_bp

def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(proxy_bp)
    app.register_blueprint(version_bp)