from flask import Blueprint
from routes.technicalAndRepairServices.electronicsRepair import electrical_repair
from routes.technicalAndRepairServices.homeService import home_service



technical_bp = Blueprint(name="technical", import_name=__name__, url_prefix="technical")


technical_bp.add_url_rule(rule="/electrical", endpoint="electrical", view_func=electrical_repair, methods=["POST"])
technical_bp.add_url_rule(rule="/home", endpoint="home", view_func=home_service, methods=["POST"])