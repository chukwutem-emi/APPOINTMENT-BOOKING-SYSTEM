from routes.utils.oauth2Callback import oauth2callback
from flask import Blueprint
from routes.utils.startOauth import start_oauth
from flask_cors import CORS


book_app_bp = Blueprint(name="bookApp", import_name=__name__, url_prefix="/bookApp")
CORS(
    book_app_bp,
    origins=["https://booksmart-ten.vercel.app"],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)
book_app_bp.add_url_rule(rule="/oauth2callback", endpoint="oauth2callback", view_func=oauth2callback, methods=["GET", "OPTIONS"])
book_app_bp.add_url_rule(rule="/start-Oauth", endpoint="start-Oauth", view_func=start_oauth, methods=["GET", "OPTIONS"])