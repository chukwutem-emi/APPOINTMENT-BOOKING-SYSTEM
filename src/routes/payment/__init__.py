from flask import Blueprint
from .callback import payment_callback
from .webhook import paystack_webhook

payment_bp = Blueprint(name="payment", import_name=__name__)


payment_bp.add_url_rule(rule="/callback", endpoint="callback", view_func=payment_callback)
payment_bp.add_url_rule(rule="/webhook", endpoint="webhook", view_func=paystack_webhook)