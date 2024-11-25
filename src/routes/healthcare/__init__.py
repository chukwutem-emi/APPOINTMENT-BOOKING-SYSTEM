from flask import Blueprint
from .consultation import consultation_session
from .counselingSessions import counseling_session
from .dentalAppointment import dental_session
from .physiotherapySessions import physiotherapy_session
from .vaccinationAppointment import vaccination_session 



health_bp = Blueprint(name="healthcare", import_name=__name__)


health_bp.add_url_rule(rule="/consult", endpoint="consult", view_func=consultation_session)
health_bp.add_url_rule(rule="/counseling", endpoint="counseling", view_func=counseling_session)
health_bp.add_url_rule(rule="/dental", endpoint="dental", view_func=dental_session)
health_bp.add_url_rule(rule="/physiotherapy", endpoint="physiotherapy", view_func=physiotherapy_session)
health_bp.add_url_rule(rule="/vaccination", endpoint="vaccination", view_func=vaccination_session)