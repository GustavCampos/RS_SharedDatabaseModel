from flask import Flask
from .controllers.client import client_bp
from .controllers.bank_accounts import bank_account_bp

def register_routes(app: Flask):
    app.register_blueprint(client_bp)
    app.register_blueprint(bank_account_bp)