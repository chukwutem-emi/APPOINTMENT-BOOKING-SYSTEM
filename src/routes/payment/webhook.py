from flask import request, jsonify, make_response
import os
import hashlib
import hmac
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY=os.getenv("PAYSTACK_SECRET_KEY")

def paystack_webhook():
    if request.method == "OPTIONS":
        return make_response("", 204)
    # getting the payment signature fro the headers
    paystack_signature =request.headers.get("x-paystack-signature")

    # The raw request data
    request_data = request.get_data()

    if  not verify_paystack_signature(request_data, paystack_signature):
        return jsonify({"error":"Invalid signature"}), 400
    
    # processing the event

    event_data = request.json
    event_type = event_data.get("event")

    if event_type == "charge.success":
        print("payment was successful:", event_data)
    
    return jsonify({"status":"success"}), 200

def verify_paystack_signature(payload, signature):
    """Verify the webhook signature from paystack."""
    computed_signature = hmac.new(
        key=bytes(PAYSTACK_SECRET_KEY, "utf-8"),
        msg=payload,
        digestmod=hashlib.sha512
    ).hexdigest()

    return hmac.compare_digest(computed_signature, signature)