from routes.utils.oauth2Callback import oauth2callback
from flask import Blueprint


book_app_bp = Blueprint(name="bookApp", import_name=__name__, url_prefix="bookApp")

book_app_bp.add_url_rule(rule="/oauth2callback", endpoint="oauth2callback", view_func=oauth2callback)