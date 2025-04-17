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

bp = Blueprint("api", __name__)

bp.register_blueprint(auth_bp)
bp.register_blueprint(user_bp)
bp.register_blueprint(edu_bp)
bp.register_blueprint(health_bp)
bp.register_blueprint(pro_service_bp)
bp.register_blueprint(technical_bp)
bp.register_blueprint(appointment_act_bp)
bp.register_blueprint(payment_bp)
bp.register_blueprint(book_app_bp)
