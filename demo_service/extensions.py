from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from demo_service import models
from demo_service.systems.authentication import Authentication
from demo_service.systems.mailer import Mailer
from demo_service.systems.session_manager import SessionManager

db = SQLAlchemy(metadata=models.Base.metadata)
session_manager = SessionManager(db)
mailer = Mailer()
authentication = Authentication(mailer, db)

def init_app(app: Flask):
    db.init_app(app)
    session_manager.init_app(app)
    mailer.init_app(app)
    authentication.init_app(app)