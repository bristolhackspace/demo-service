from datetime import datetime, timezone

from flask import Blueprint, render_template, request
import uuid
from werkzeug.exceptions import BadRequest

from demo_service.extensions import db
from demo_service.models.onboarding import Onboarding

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("main/index.html.j2")

@bp.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    return render_template("main/agreement.html.j2")
    with db.session.begin():
        now = datetime.now(timezone.utc)
        flow_id = request.args.get("flow_id")
        onboarding = db.session.get(Onboarding, flow_id)
        if onboarding is None:
            onboarding = Onboarding(
                id=uuid.uuid4(),
                start_time=now,
                current_page="terms"
            )
            db.session.add(onboarding)

        if onboarding.current_page == "terms":
            pass
        elif onboarding.current_page == "":
            pass
        

@bp.app_errorhandler(BadRequest)
def handle_bad_request(exception):
    return render_template("main/exception.html.j2", exception=exception)