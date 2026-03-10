from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy


from .mailer import BaseMailer
from .discourse_connect import DiscourseConnect
from .session_manager import SessionManager

class HackspaceSystems:
    def __init__(self, db: SQLAlchemy, app: Flask):
        self.db = db
        self.mailer = BaseMailer.build(self, app)
        self.session = SessionManager(self, app)
        self.discourse = DiscourseConnect(self, app)


class HackspaceExtension:
    def __init__(self, db: SQLAlchemy, app: Flask | None = None):
        self.db = db
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.extensions["hackspace"] = HackspaceSystems(self.db, app)

    @property
    def systems(self) -> HackspaceSystems:
        return current_app.extensions["hackspace"]
    
    @property
    def mailer(self) -> BaseMailer:
        return self.systems.mailer
    
    @property
    def session(self) -> SessionManager:
        return self.systems.session
    
    @property
    def discourse(self) -> DiscourseConnect:
        return self.systems.discourse