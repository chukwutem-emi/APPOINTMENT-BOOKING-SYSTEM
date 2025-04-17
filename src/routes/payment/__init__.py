from flask import Blueprint
from routes.payment.callback import payment_callback
from routes.payment.webhook import paystack_webhook

payment_bp = Blueprint(name="payment", import_name=__name__, url_prefix="payment")


payment_bp.add_url_rule(rule="/callback", endpoint="callback", view_func=payment_callback, methods=["GET"])
payment_bp.add_url_rule(rule="/webhook", endpoint="webhook", view_func=paystack_webhook, methods=["POST"])