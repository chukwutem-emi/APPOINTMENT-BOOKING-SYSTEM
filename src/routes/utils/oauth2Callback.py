from flask import request, jsonify, current_app
from routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os
import base64
import json
import tempfile
from tables.dbModels import User, db

load_dotenv()

b64_cred = os.getenv("GOOGLE_CREDENTIALS_B64")
# decode from base64
decode_json = base64.b64decode(b64_cred).decode("utf-8")
credentials_dict = json.loads(decode_json)
print("Decoded credentials dict:", credentials_dict)

SCOPE = [SCOPE]
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
if not credentials_dict:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

def oauth2callback():
    state = request.args.get("state")
    code = request.args.get("code")

    if not state or not code:
            return jsonify({"error": "Missing state or code parameters"}), 400

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        json.dump(credentials_dict, temp_file)
        temp_file_path = temp_file.name
    try:
        flow = Flow.from_client_secrets_file(
            client_secrets_file=temp_file_path, 
            scopes=SCOPE,
            redirect_uri = REDIRECT_URI
            )
        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        user = User.query.get(state)
        if not user:
             return jsonify({"error":"user not found!"}), 404
        
        user.google_token = creds.to_json()
        db.session.commit()
        return "Authentication successful!, You may close this tab."
    except Exception as e:
         current_app.logger.exception("auth callback failed!"), 500
         return jsonify({"error":str(e)}), 500
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)