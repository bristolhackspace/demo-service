from flask import Flask
from . import main

def init_app(app: Flask):
    app.register_blueprint(main.bp)