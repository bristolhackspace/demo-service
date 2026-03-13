from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import LocalProxy

from demo_service import models
from demo_service.systems import HackspaceSystems

db = SQLAlchemy(metadata=models.Base.metadata)

def get_hs_systems() -> HackspaceSystems:
    return current_app.extensions["hackspace"]

hs = LocalProxy(get_hs_systems)


def init_app(app: Flask):
    db.init_app(app)
    app.extensions["hackspace"] = HackspaceSystems(db, app)