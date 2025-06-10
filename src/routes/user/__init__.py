from flask import Blueprint
from routes.user.getAUser import get_user
from routes.user.getAllUsers import get_users
from routes.user.updateUser import update_user
from routes.user.deleteUser import delete_user
from routes.user.promoteUser import promote_user
from routes.user.deleteAll import delete_all_users
from flask_cors import CORS
from routes.utils.constants import FRONT_END_URL

user_bp = Blueprint(name="a_user_bp", import_name=__name__, url_prefix="user_bp")
CORS(
    user_bp,
    origins=[FRONT_END_URL],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)

user_bp.add_url_rule(rule="/user", endpoint="user", view_func=get_user, methods=["GET"])
user_bp.add_url_rule(rule="/users", endpoint="users", view_func=get_users, methods=["GET"])
user_bp.add_url_rule(rule="/update", endpoint="update", view_func=update_user, methods=["PUT"])
user_bp.add_url_rule(rule="/delete", endpoint="delete", view_func=delete_user, methods=["DELETE"])
user_bp.add_url_rule(rule="/promote", endpoint="promote", view_func=promote_user, methods=["PUT"])
user_bp.add_url_rule(rule="/delete_all", endpoint="delete_all", view_func=delete_all_users, methods=["DELETE"])