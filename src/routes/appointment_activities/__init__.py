from flask import Blueprint
from .getAllUsersAppointmentDetails import users_appointment_details
from .updateUserAppointmentDetails import update_user_appointment_details
from .getUserAppointmentDetails import a_user_appointment_details
from .deleteUserAppointmentDetails import delete_user_appointment_details
from flask_cors import CORS

appointment_act_bp = Blueprint(name="appointment_act", import_name=__name__, url_prefix="/appointment-act")

CORS(
    appointment_act_bp,
    origins=["http://localhost:1234"],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)
appointment_act_bp.add_url_rule(rule="/users-appointment", endpoint="users-appointment", view_func=users_appointment_details, methods=["GET", "OPTIONS"])
appointment_act_bp.add_url_rule(rule="/update-user-appointment", endpoint="update-user-appointment", view_func=update_user_appointment_details, methods=["PUT", "OPTIONS"])
appointment_act_bp.add_url_rule(rule="/user-appointment", endpoint="user-appointment", view_func=a_user_appointment_details, methods=["GET", "OPTIONS"])
appointment_act_bp.add_url_rule(rule="/delete-appointment", endpoint="delete-appointment", view_func=delete_user_appointment_details, methods=["DELETE", "OPTIONS"])
