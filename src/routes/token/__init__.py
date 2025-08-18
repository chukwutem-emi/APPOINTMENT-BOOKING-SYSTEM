from flask import Blueprint
from routes.token.clearGoogleToken import clear_google_token
from flask_cors import CORS
from routes.utils.constants import FRONT_END_URL

token_bp = Blueprint("token", __name__, url_prefix="/token")
CORS(
    token_bp,
    origins=[FRONT_END_URL],
    methods=["POST", "GET", "DELETE", "PUT", "OPTIONS"],
    allow_headers=["Authorization", "access-token", "Content-Type"],
    supports_credentials=True
)

token_bp.add_url_rule(rule="/clear-token", endpoint="/clear-token", view_func=clear_google_token, methods=["PUT", "OPTIONS"])