from flask import Blueprint, render_template

from demo_service.middleware import require_login

bp = Blueprint("main", __name__, url_prefix="/")

bp.before_request(require_login)

@bp.route("/")
def index():
    return render_template("main/index.html.j2")