from flask import Blueprint, request
from sqlalchemy.dialects.postgresql import insert
from werkzeug.exceptions import BadRequest

from demo_service.extensions import db
from demo_service.middleware import require_token
from demo_service.models import Member

bp = Blueprint("api", __name__, url_prefix="/api/v1")

bp.before_request(require_token)

@bp.route("/members/<ext_id>", methods=["GET", "PUT"])
def member(ext_id):
    if request.method == "GET":
        member = db.get_or_404(Member, ext_id)
        return {
            "name": member.name,
            "email": member.email,
            "consent": member.email_consent
        }
    else:
        fields = request.json
        if not isinstance(fields, dict):
            raise BadRequest("Invalid JSON structure")

        stmt = insert(Member).values(
            ext_id=ext_id,
            **fields
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[Member.ext_id],
            set_=fields
        )
        db.session.execute(stmt)
        db.session.commit()
        return "OK"