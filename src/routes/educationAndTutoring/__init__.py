from flask import Blueprint
from routes.educationAndTutoring.academicAdvising import academic_advising
from routes.educationAndTutoring.careerCounseling import career_counseling
from routes.educationAndTutoring.oneOnOneTutoringSessions import one_on_one_tutoring

edu_bp = Blueprint(name="/education_bp", import_name=__name__)

edu_bp.add_url_rule(rule="/academic", endpoint="academic", view_func=academic_advising)
edu_bp.add_url_rule(rule="/career", endpoint="career", view_func=career_counseling)
edu_bp.add_url_rule(rule="/tutoring", endpoint="tutoring", view_func=one_on_one_tutoring)
