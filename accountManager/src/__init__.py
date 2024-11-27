from flask import Flask
from .controllers.client import client_bp

def register_routes(app: Flask):
    app.register_blueprint(client_bp)