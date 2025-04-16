from flask import request, redirect
from src.routes.utils.constants import SCOPE
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os

load_dotenv()

SCOPE = [SCOPE]
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables.")

def start_oauth():
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=GOOGLE_CREDENTIALS_JSON,
        scopes=SCOPE
        )
    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt="consent")

    # Redirect the user to the Google OAuth URL
    return redirect(location=auth_url)
