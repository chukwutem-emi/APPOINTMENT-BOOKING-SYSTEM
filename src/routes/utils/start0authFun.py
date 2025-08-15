from flask import request, jsonify, current_app, redirect
from routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import Flow
from routes.utils.loadGoogleCred import load_google_credentials
import traceback
import os


credentials_dict = load_google_credentials()
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


def oauth_function(user_id):
    current_app.logger.info("start_oauth endpoint called")
    try:
        flow = Flow.from_client_config(
            client_config=credentials_dict,
            scopes=SCOPE if isinstance(SCOPE, list) else [SCOPE]
            )
        flow.redirect_uri = REDIRECT_URI
        print("Loaded credentials dict keys:", credentials_dict.keys())
        print("Redirect URI:", REDIRECT_URI)
        print("Scope:", SCOPE)



        # Generate the authorization URL
        auth_url, _= flow.authorization_url(
            access_type = "offline",
            include_granted_scopes = True,
            state = str(user_id),
            prompt = "consent select_account"
        )
        current_app.logger.info(f"Generated Google OAuth URL: {auth_url}")
        # If request came from browser (not from fetch/AJAX), redirect
        if "text/html" in request.headers.get("Accept", ""):
            return redirect(auth_url)

        # Redirect the user to the Google OAuth URL
        return jsonify({"Authentication_url":auth_url}), 201
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Failed to start OAuth flow")
        return {"error": str(e)}, 500
