from routes.authentication import auth_bp
from flask import Blueprint
from routes.user import user_bp
from routes.educationAndTutoring import edu_bp
from routes.healthcare import health_bp
from routes.professionalServices import pro_service_bp
from routes.technicalAndRepairServices import technical_bp
from routes.appointment_activities import appointment_act_bp
from routes.payment import payment_bp
from routes.utils import book_app_bp
from routes.token import token_bp

blue_p = Blueprint("api", __name__)

blue_p.register_blueprint(auth_bp)
blue_p.register_blueprint(user_bp)
blue_p.register_blueprint(edu_bp)
blue_p.register_blueprint(health_bp)
blue_p.register_blueprint(pro_service_bp)
blue_p.register_blueprint(technical_bp)
blue_p.register_blueprint(appointment_act_bp)
blue_p.register_blueprint(payment_bp)
blue_p.register_blueprint(book_app_bp)
blue_p.register_blueprint(token_bp)
