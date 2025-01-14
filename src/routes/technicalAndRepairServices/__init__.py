from flask import Blueprint
from .electronicsRepair import electrical_repair
from .homeService import home_service



technical_bp = Blueprint(name="technical", import_name=__name__)


technical_bp.add_url_rule(rule="/electrical", endpoint="electrical", view_func=electrical_repair)
technical_bp.add_url_rule(rule="/home", endpoint="home", view_func=home_service)