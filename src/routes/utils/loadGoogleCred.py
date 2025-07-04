import base64
import json
import os
from flask import current_app
from dotenv import load_dotenv

load_dotenv()

def load_google_credentials():
    b64_cred = os.getenv("GOOGLE_CREDENTIALS_B64")

    if not b64_cred:
        raise ValueError("GOOGLE_CREDENTIALS_B64 is not set in environment variables.")

    try:
        decode_json = base64.b64decode(b64_cred).decode("utf-8")
        credentials_dict = json.loads(decode_json)
    except Exception as e:
        raise ValueError(f"Failed to decode or parse credentials: {e}")

    required_fields = ["client_id", "client_secret", "auth_uri", "token_uri"]
    if "web" not in credentials_dict:
        raise ValueError(f"Missing 'installed' key in credentials JSON: {credentials_dict}")
    web_cred = credentials_dict["web"]
    for field in required_fields:
        if field not in web_cred:
            raise ValueError(f"Missing required field in credentials: {field}")

    return web_cred
