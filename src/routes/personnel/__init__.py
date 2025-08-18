from flask import Blueprint
from routes.personnel.createPersonnel import create_personnel
from flask_cors import CORS
from .deletePersonnel import delete_personnel
from .getAllPersonnel import get_all_personnel
from .getPersonnel import get_personnel
from .updatePersonnel import update_personnel
from routes.utils.constants import FRONT_END_URL

personnel_bp = Blueprint(name="personnel", import_name=__name__, url_prefix="/personnel-bp")

CORS(
    personnel_bp,
    origins=[FRONT_END_URL],
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "access-token"],
)

personnel_bp.add_url_rule(rule="/personnel", endpoint="personnel", view_func=create_personnel, methods=["POST", "OPTIONS"])
personnel_bp.add_url_rule(rule="/delete-personnel", endpoint="/delete-personnel", view_func=delete_personnel, methods=["DELETE", "OPTIONS"])
personnel_bp.add_url_rule(rule="/all-personnel", endpoint="all-personnel", view_func=get_all_personnel, methods={"GET", "OPTIONS"})
personnel_bp.add_url_rule(rule="/one-personnel", endpoint="one-personnel", view_func=get_personnel, methods=["GET", "OPTIONS"])
personnel_bp.add_url_rule(rule="/update-personnel", endpoint="update-personnel", view_func=update_personnel, methods=["PUT", "OPTIONS"])