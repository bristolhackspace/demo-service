from __future__ import annotations

from datetime import datetime, timedelta, timezone
import functools
from flask import Flask, Response, current_app, g, request, after_this_request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from typing import TYPE_CHECKING
import secrets
import uuid

from demo_service.helpers import as_timedelta
from demo_service.models import Session, Member


class SessionManager():
    def __init__(self, db: SQLAlchemy, app: Flask):
        self.db = db

        self.cookie_name: str = app.config.get("HS_SESSION_NAME", "id")
        self.cookie_max_age = as_timedelta(
            app.config.get("HS_SESSION_MAX_AGE", timedelta(days=1))
        )
        self.cookie_secure: bool = app.config.get("HS_SESSION_SECURE", False)

        self.elevated_auth_expiry = as_timedelta(
            app.config.get("HS_ELEVATED_AUTH_EXPIRY", timedelta(minutes=20))
        )

        app.before_request(self._load_session)


    def _load_session(self):
        parts = request.cookies.get(self.cookie_name, "").split(":")
        if len(parts) != 2:
            return
        id_, secret = parts

        session = self.db.session.get(Session, uuid.UUID(hex=id_))

        if session is None:
            return

        if not secrets.compare_digest(session.secret_hash, self.hash_secret(secret)):
            return

        now = datetime.now(timezone.utc)

        if session.last_active > (now - self.cookie_max_age):
            session.last_active = now
            after_this_request(functools.partial(self.update_cookie, session, secret))
        else:
            self.db.session.delete(session)
        self.db.session.commit()

    def authenticate(self, member: Member):
        now = datetime.now(timezone.utc)
        session = self.current_session

        if session and session.member != member:
            self.db.session.delete(session)
            self.db.session.commit()
            session = None

        if session is None:
            session = Session(id=uuid.uuid4(), created=now, member=member, last_active=now)
            self.db.session.add(session)
            g.hs_session = session

        # Rotate secret
        secret = secrets.token_urlsafe()
        session.secret_hash = self.hash_secret(secret)

        self.db.session.commit()

        after_this_request(functools.partial(self.update_cookie, session, secret))

    def update_cookie(
        self, session: Session, secret: str, response: Response
    ) -> Response:
        value = f"{session.id.hex}:{secret}"
        response.set_cookie(
            key=self.cookie_name,
            value=value,
            max_age=self.cookie_max_age,
            httponly=True,
            secure=self.cookie_secure,
        )
        return response

    @staticmethod
    def hash_secret(secret: str | bytes) -> str:
        if isinstance(secret, str):
            secret = secret.encode("utf-8")
        return hashlib.sha256(secret).hexdigest()

    @property
    def current_session(self) -> Session | None:
        return g.get("hs_session")
