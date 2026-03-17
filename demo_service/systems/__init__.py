from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import gocardless_pro


from .mailer import BaseMailer
from .discourse_connect import DiscourseConnect
from .session_manager import SessionManager

class HackspaceSystems:
    def __init__(self, db: SQLAlchemy, app: Flask):
        self.db = db
        self.mailer = BaseMailer.build(app)
        self.session = SessionManager(self.db, app)
        self.discourse = DiscourseConnect(self.db, self.session, app)
        self.gocardless = gocardless_pro.Client(
            app.config["GOCARDLESS_ACCESS_TOKEN"],
            environment=app.config.get("GOCARDLESS_ENVIRONMENT", "sandbox")
        )