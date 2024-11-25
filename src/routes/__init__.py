from .authentication import auth_bp
from flask import Blueprint
from .user import user_bp
from .educationAndTutoring import edu_bp
from .healthcare import health_bp
from .professionalServices import pro_service_bp
from .technicalAndRepairServices import technical_bp
from .appointment_activities import appointment_act_bp
from .payment import payment_bp
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
