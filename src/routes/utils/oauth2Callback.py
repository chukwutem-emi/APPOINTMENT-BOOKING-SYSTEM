from flask import request, redirect
from routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SCOPE = [SCOPE]
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

def oauth2callback():
    state = request.args.get("state")
    code = request.args.get("code")
    flow = Flow.from_client_secrets_file(
        client_secrets_file=GOOGLE_CREDENTIALS_JSON, 
        scopes=SCOPE,
        redirect_uri = REDIRECT_URI
        )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    token_path = os.path.join(os.getcwd(), f"token_{state}.json")
    
    with open(token_path, mode="w") as token:
        token.write(creds.to_json())

    return "Authentication successful!, You may close this tab."