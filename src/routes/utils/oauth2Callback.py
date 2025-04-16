from src.flaskFile import app
from flask import request, redirect
from src.routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SCOPE = [SCOPE]
if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

@app.route(rule="/oauth2callback")
def oauth2callback(json_file):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=GOOGLE_CREDENTIALS_JSON, 
        scopes=SCOPE
        )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    with open(token_path=json_file, mode="w") as token:
        token.write(creds.to_json())

    return "Authentication successful!, You may close this tab."