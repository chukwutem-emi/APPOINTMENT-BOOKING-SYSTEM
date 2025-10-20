from flask import Blueprint
from routes.technicalAndRepairServices.electronicsRepair import electrical_repair
from routes.technicalAndRepairServices.homeService import home_service
from flask_cors import CORS


technical_bp = Blueprint(name="technical", import_name=__name__, url_prefix="technical")
CORS(
    technical_bp,
    origins=["https://booksmart-ten.vercel.app", "http://localhost:1234"],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "access-token"]
)

technical_bp.add_url_rule(rule="/electrical", endpoint="electrical", view_func=electrical_repair, methods=["POST", "OPTIONS"])
technical_bp.add_url_rule(rule="/home", endpoint="home", view_func=home_service, methods=["POST", "OPTIONS"])