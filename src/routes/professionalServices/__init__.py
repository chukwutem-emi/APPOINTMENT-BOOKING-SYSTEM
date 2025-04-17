from routes.professionalServices.businessConsultations import business_consultation
from routes.professionalServices.financialAdvisory import financial_advisory
from routes.professionalServices.realEstateAgentAppointment import  real_estate_agent
from flask import Blueprint

pro_service_bp = Blueprint(name="professional", import_name=__name__, url_prefix="professional")


pro_service_bp.add_url_rule(rule="/business", endpoint="business", view_func=business_consultation, methods=["POST"])
pro_service_bp.add_url_rule(rule="/financial", endpoint="financial", view_func=financial_advisory, methods=["POST"])
pro_service_bp.add_url_rule(rule="/real_estate", endpoint="real_estate", view_func=real_estate_agent, methods=["POST"])