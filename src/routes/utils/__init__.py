from routes.utils.oauth2Callback import oauth2callback
from flask import Blueprint
from routes.utils.startOauth import start_oauth


book_app_bp = Blueprint(name="bookApp", import_name=__name__, url_prefix="bookApp")

book_app_bp.add_url_rule(rule="/oauth2callback", endpoint="oauth2callback", view_func=oauth2callback)
book_app_bp.add_url_rule(rule="/startOauth", endpoint="startOauth", view_func=start_oauth)