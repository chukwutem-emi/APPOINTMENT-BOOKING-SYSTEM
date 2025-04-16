from flask import Blueprint
from src.routes.user.getAUser import get_user
from src.routes.user.getAllUsers import get_users
from src.routes.user.updateUser import update_user
from src.routes.user.deleteUser import delete_user
from src.routes.user.promoteUser import promote_user
from src.routes.user.deleteAll import delete_all_users

user_bp = Blueprint(name="a_user_bp", import_name=__name__)

user_bp.add_url_rule(rule="/user", endpoint="user", view_func=get_user)
user_bp.add_url_rule(rule="/users", endpoint="users", view_func=get_users)
user_bp.add_url_rule(rule="/update", endpoint="update", view_func=update_user)
user_bp.add_url_rule(rule="/delete", endpoint="delete", view_func=delete_user)
user_bp.add_url_rule(rule="/promote", endpoint="promote", view_func=promote_user)
user_bp.add_url_rule(rule="/delete_all", endpoint="delete_all", view_func=delete_all_users)