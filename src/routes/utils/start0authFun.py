from flask import request, redirect, current_app
from routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os
import base64
import json
import tempfile

load_dotenv()

SCOPE = [SCOPE]
b64_cred = os.getenv("GOOGLE_CREDENTIALS_B64")
# decode from base64
decode_json = base64.b64decode(b64_cred).decode("utf-8")
credentials_dict = json.loads(decode_json)
print("Decoded credentials dict:", credentials_dict)

REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
if not credentials_dict:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

def oauth_function(user_id):
    current_app.logger.info("start_oauth endpoint called")
    try:
        flow = Flow.from_client_config(
            client_secrets_file=credentials_dict,
            scopes=SCOPE,
            redirect_uri = REDIRECT_URI
            )
        # Generate the authorization URL
        auth_url, _= flow.authorization_url(
            access_type = "offline",
            include_granted_scopes = "true",
            state = str(user_id),
            prompt = "consent"
        )
        current_app.logger.info(f"Generated Google OAuth URL: {auth_url}")


        # Redirect the user to the Google OAuth URL
        return redirect(auth_url)
    except Exception as e:
        current_app.logger.exception("Failed to start OAuth flow")
        return {"error": str(e)}, 500
