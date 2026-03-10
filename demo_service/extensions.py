from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from demo_service import models
from demo_service.systems.session_manager import SessionManager
from demo_service.systems import HackspaceExtension

db = SQLAlchemy(metadata=models.Base.metadata)
hs = HackspaceExtension(db)


def init_app(app: Flask):
    db.init_app(app)
    hs.init_app(app)