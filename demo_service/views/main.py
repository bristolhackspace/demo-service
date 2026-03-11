from flask import Blueprint, render_template
from werkzeug.exceptions import BadRequest

from demo_service.middleware import require_login

bp = Blueprint("main", __name__, url_prefix="/")

bp.before_request(require_login)

@bp.route("/")
def index():
    return render_template("main/index.html.j2")

@bp.app_errorhandler(BadRequest)
def handle_bad_request(exception):
    return render_template("main/exception.html.j2", exception=exception)