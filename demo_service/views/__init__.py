from flask import Flask
from . import main, api

def init_app(app: Flask):
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)