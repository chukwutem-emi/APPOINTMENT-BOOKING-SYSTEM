from flask import Blueprint
from routes.authentication.login import sign_in
from routes.authentication.register import sign_up

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.add_url_rule("/login", view_func=sign_in)
auth_bp.add_url_rule("/register", view_func=sign_up, methods=["POST"])