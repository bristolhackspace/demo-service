from __future__ import annotations

import base64
from typing import TYPE_CHECKING, cast

from datetime import datetime, timedelta, timezone
from flask import Flask, Request, session
import hashlib
import hmac
from secrets import token_urlsafe
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from urllib.parse import urlencode, parse_qs
from yarl import URL

from demo_service.models import Member
from demo_service.helpers import as_timedelta

if TYPE_CHECKING:
    from demo_service.systems.session_manager import SessionManager


class DiscourseConnectError(Exception):
    pass


class DiscourseConnect():
    def __init__(self, db: SQLAlchemy, session: SessionManager, app: Flask):
        self.db = db
        self.session = session

        self.sso_url: str = app.config["SSO_URL"]
        self.sso_secret = app.config["SSO_SECRET"].encode("utf-8")
        self.sso_expiry = as_timedelta(app.config.get("SSO_EXPIRY", timedelta(minutes=15)))


    def begin_login(self, return_url: str) -> str:

        nonce = token_urlsafe()
        expiry = datetime.now(timezone.utc) + self.sso_expiry

        session["nonce"] = nonce
        session["nonce_expiry"] = int(expiry.timestamp())

        query = urlencode({
            "nonce": nonce,
            "return_sso_url": str(return_url)
        })

        response_encoded = base64.b64encode(query.encode("utf-8"))
        response_digest = hmac.new(self.sso_secret, response_encoded, hashlib.sha256).hexdigest()

        redirect_url = URL(self.sso_url).with_query(
            {
                "sso": response_encoded.decode("utf-8"),
                "sig": response_digest,
            }
        )

        return str(redirect_url)

    def complete_login(self, request: Request) -> bool:
        sso = request.args.get("sso")
        sig = request.args.get("sig")

        if sso is None or sig is None:
            return False

        # Check the signature is valid
        digest = hmac.new(self.sso_secret, sso.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(digest, sig):
            return False

        # Extract arguments from sso
        qs = base64.b64decode(sso).decode("utf-8")
        args = parse_qs(qs)
        nonce = args["nonce"][0]

        now = datetime.now(timezone.utc)
        nonce_expiry = datetime.fromtimestamp(session.get("nonce_expiry", 0), timezone.utc)
        # if nonce_expiry < now or session.get("nonce") != nonce:
        #     return False

        ext_id = int(args["external_id"][0])
        email = args["email"][0]
        name = args["name"][0]

        member = self._find_or_create_member(ext_id, email, name)

        self.session.authenticate(member)

        return True

    def _find_or_create_member(self, ext_id: int, email: str, name: str) -> Member:
        stmt = insert(Member).values(
            ext_id=ext_id,
            name=name,
            email=email
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[Member.ext_id],
            set_=dict(name=name, email=email)
        ).returning(Member)

        orm_stmt = sa.select(Member).from_statement(stmt).execution_options(populate_existing=True)
        # Typecast as first() can return Null but we know the statement will always return something
        return cast(Member, self.db.session.scalars(orm_stmt).first())
