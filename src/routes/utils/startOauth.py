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
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
if not credentials_dict:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

def start_oauth(user_id):
    current_app.logger.info("start_oauth endpoint called")
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        json.dump(credentials_dict, temp_file)
        temp_file_path = temp_file.name
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file=temp_file_path,
            scopes=SCOPE,
            redirect_uri = REDIRECT_URI
            )
        # Generate the authorization URL
        auth_url, _= flow.authorization_url(
            access_type = "offline",
            include_granted_scopes = "true",
            state = user_id
        )

        # Redirect the user to the Google OAuth URL
        return redirect(auth_url)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
