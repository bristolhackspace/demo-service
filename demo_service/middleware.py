
from flask import Flask, redirect, request
from werkzeug import Response
from werkzeug.exceptions import BadRequest

from demo_service.extensions import hs

# Below are functions which can be used with the various Flask `before_request` hooks.

def require_login() -> Response | None:
    # This will do nothing if `sig` or `sso` query arguments are missing, so no
    # harm in checking on every request
    return
    hs.discourse.complete_login(request)

    session = hs.session.current_session

    if session is None:
        if request.args.get("sso") or request.args.get("sig"):
            raise BadRequest("Something went wrong when trying to log you in. Please contact the Hackspace committee if this persists")
        return redirect(hs.discourse.begin_login(request.url))
    
def require_token() -> Response | None:
    return