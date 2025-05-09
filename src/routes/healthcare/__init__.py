from flask import Blueprint
from routes.healthcare.consultation import consultation_session
from routes.healthcare.counselingSessions import counseling_session
from routes.healthcare.dentalAppointment import dental_session
from routes.healthcare.physiotherapySessions import physiotherapy_session
from routes.healthcare.vaccinationAppointment import vaccination_session



health_bp = Blueprint(name="healthcare", import_name=__name__, url_prefix="/healthcare")


health_bp.add_url_rule(rule="/consult", endpoint="consult", view_func=consultation_session, methods=["POST"])
health_bp.add_url_rule(rule="/counseling", endpoint="counseling", view_func=counseling_session, methods=["POST"])
health_bp.add_url_rule(rule="/dental", endpoint="dental", view_func=dental_session, methods=["POST"])
health_bp.add_url_rule(rule="/physiotherapy", endpoint="physiotherapy", view_func=physiotherapy_session, methods=["POST"])
health_bp.add_url_rule(rule="/vaccination", endpoint="vaccination", view_func=vaccination_session, methods=["POST"])