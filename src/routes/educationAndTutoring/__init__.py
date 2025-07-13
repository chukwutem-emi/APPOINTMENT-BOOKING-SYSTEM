from flask import Blueprint
from routes.educationAndTutoring.academicAdvising import academic_advising
from routes.educationAndTutoring.careerCounseling import career_counseling
from routes.educationAndTutoring.oneOnOneTutoringSessions import one_on_one_tutoring
from flask_cors import CORS
from routes.utils.constants import FRONT_END_URL

edu_bp = Blueprint(name="/education_bp", import_name=__name__, url_prefix="education_bp")

CORS(
    edu_bp,
    origins=["http://localhost:1234"],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)

edu_bp.add_url_rule(rule="/academic", endpoint="academic", view_func=academic_advising, methods=["POST", "OPTIONS"])
edu_bp.add_url_rule(rule="/career", endpoint="career", view_func=career_counseling, methods=["POST", "OPTIONS"])
edu_bp.add_url_rule(rule="/tutoring", endpoint="tutoring", view_func=one_on_one_tutoring, methods=["POST", "OPTIONS"])
