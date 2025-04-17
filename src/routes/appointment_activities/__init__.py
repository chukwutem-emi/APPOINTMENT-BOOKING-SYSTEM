from flask import Blueprint
from .getAllUsersAppointmentDetails import users_appointment_details
from .updateUserAppointmentDetails import update_user_appointment_details
from .getUserAppointmentDetails import a_user_appointment_details
from .deleteUserAppointmentDetails import delete_user_appointment_details


appointment_act_bp = Blueprint(name="appointment_act", import_name=__name__, url_prefix="/appointment_act")

appointment_act_bp.add_url_rule(rule="/users_appointment", endpoint="users_appointment", view_func=users_appointment_details, methods=["GET"])
appointment_act_bp.add_url_rule(rule="/update_user_appointment", endpoint="update_user_appointment", view_func=update_user_appointment_details, methods=["PUT"])
appointment_act_bp.add_url_rule(rule="/user_appointment", endpoint="user_appointment", view_func=a_user_appointment_details, methods=["GET"])
appointment_act_bp.add_url_rule(rule="/delete_appointment", endpoint="delete_appointment", view_func=delete_user_appointment_details, methods=["DELETE"])
