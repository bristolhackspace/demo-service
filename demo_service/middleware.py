
from flask import Flask, redirect, request
from werkzeug import Response

from demo_service.extensions import hs

# Below are functions which can be used with the various Flask `before_request` hooks.

def require_login() -> Response | None:
    # This will do nothing if `sig` or `sso` query arguments are missing, so no
    # harm in checking on every request
    hs.discourse.complete_login(request)

    session = hs.session.current_session

    if session is None:
        return redirect(hs.discourse.begin_login(request.url))