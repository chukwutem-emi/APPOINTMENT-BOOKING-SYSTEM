from flask import Blueprint
from routes.authentication.login import sign_in
from routes.authentication.register import sign_up
from flask_cors import CORS
from routes.utils.constants import FRONT_END_URL

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CORS(
    auth_bp,
    origins=[FRONT_END_URL],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)

auth_bp.add_url_rule("/login", view_func=sign_in, methods=["POST", "OPTIONS"])
auth_bp.add_url_rule("/register", view_func=sign_up, methods=["POST", "OPTIONS"])
