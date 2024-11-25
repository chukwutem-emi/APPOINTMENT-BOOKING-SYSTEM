from flask import Blueprint
from .academicAdvising import academic_advising
from .careerCounseling import career_counseling
from .oneOnOneTutoringSessions import one_on_one_tutoring

edu_bp = Blueprint(name="/education_bp", import_name=__name__)

edu_bp.add_url_rule(rule="/academic", endpoint="academic", view_func=academic_advising)
edu_bp.add_url_rule(rule="/career", endpoint="career", view_func=career_counseling)
edu_bp.add_url_rule(rule="/tutoring", endpoint="tutoring", view_func=one_on_one_tutoring)
