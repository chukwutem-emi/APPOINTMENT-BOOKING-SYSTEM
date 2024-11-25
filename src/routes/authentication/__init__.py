from flask import Blueprint
from .login import sign_in
from .register import sign_up

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/login", view_func=sign_in)
auth_bp.add_url_rule("/register", view_func=sign_up)