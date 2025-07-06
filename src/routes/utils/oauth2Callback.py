from flask import request, jsonify, current_app
from routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import Flow
from routes.utils.loadGoogleCred import load_google_credentials
import os
import base64
import json
import tempfile
from tables.dbModels import User, db

credentials_dict = load_google_credentials()
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def oauth2callback():
    print("oauth2callback function called!")
    state = request.args.get("state")
    code = request.args.get("code")
    current_app.logger.info(f"Full request URL: {request.url}")
    current_app.logger.info(f"State parameter: {state}")
    current_app.logger.info(f"Code parameter: {code}")


    if not state or not code:
            return jsonify({"error": "Missing state or code parameters"}), 400

    try:
        flow = Flow.from_client_config(
            client_config=credentials_dict, 
            scopes=[SCOPE],
            )
        flow.redirect_uri = REDIRECT_URI
        print("SCOPES being used:", [SCOPE])


        flow.fetch_token(authorization_response=request.url)
        creds = flow.credentials
        print("SAVED CREDS JSON:", creds.to_json())
        try:
            user_id = int(state)
        except ValueError:
            return jsonify({"error": "Invalid user ID in state"}), 400
        user = User.query.get(user_id)
        current_app.logger.info(f"User type: {type(user)} - {user}")

        if not user:
            return jsonify({"error": "user not found!"}), 404

        if not hasattr(user, "google_token"):
            return jsonify({"error": "User object has no google_token attribute"}), 500
        token_json = json.loads(creds.to_json())

        # 🔧 Ensure scopes are stored as a list
        if isinstance(token_json.get("scopes"), str):
            token_json["scopes"] = [token_json["scopes"]]

        try:
            user_id = int(state)
        except ValueError:
            return jsonify({"error": "Invalid user ID in state"}), 400

        if not user:
            return jsonify({"error": "User not found!"}), 404

        user.google_token = json.dumps(token_json)
        db.session.commit()



        return "Authentication successful!, You may close this tab."
    except Exception as e:
         current_app.logger.exception("auth callback failed!")
         return jsonify({"error":str(e)}), 500
    