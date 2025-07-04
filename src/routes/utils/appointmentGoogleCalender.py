import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from routes.utils.constants import SCOPE
import base64
import json
from flask import current_app
from tables.dbModels import User, db
import traceback
from google.auth.exceptions import RefreshError


load_dotenv()

ENV = os.getenv("ENV", "development")
b64_cred = os.getenv("GOOGLE_CREDENTIALS_B64")
# decode from base64
decode_json = base64.b64decode(b64_cred).decode("utf-8")
credentials_dict = json.loads(decode_json)


SCOPES = [SCOPE]
print("DEBUG SCOPES:", SCOPES)
print("Type of SCOPES:", type(SCOPES))
if isinstance(SCOPES, list):
    print("First item:", SCOPES[0], "| type:", type(SCOPES[0]))


if not credentials_dict:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables")

def book_appointment(summary, location, description, dateTime, email, endDateTime, user_id):
    current_app.logger.info("book appointment function called!")
    creds = None
    temp_credentials_file = None
    try:
        user = User.query.get(user_id)
        if not user or not user.google_token:
            return {
                "error": f"Missing or invalid credentials for user {user_id}. "
                        f"User must authenticate via /start-auth?user_id={user_id}"
            }, 401
        stored_token = json.loads(user.google_token)
        if isinstance(stored_token["scopes"], str):
            stored_token["scopes"] = [stored_token["scopes"]]
        print("💥 Stored Token:", stored_token)

        print("💥 Stored token scopes value:", stored_token["scopes"])
        print("💥 Type of stored scopes:", type(stored_token["scopes"]))
        scopes = stored_token["scopes"]

        if isinstance(scopes, str):
            scopes = [scopes] 
        creds = Credentials(
            token=stored_token["token"],
            refresh_token=stored_token.get("refresh_token"),
            token_uri=stored_token["token_uri"],
            client_id=stored_token["client_id"],
            client_secret=stored_token["client_secret"],
            scopes=scopes,
        )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())                         # refresh

                    # store fresh token + expiry back to DB
                    user.google_token = json.dumps({
                        "token":          creds.token,
                        "refresh_token":  creds.refresh_token,
                        "token_uri":      creds.token_uri,
                        "client_id":      creds.client_id,
                        "client_secret":  creds.client_secret,
                        "scopes":         creds.scopes,
                        "expiry":         creds.expiry.isoformat() if creds.expiry else None
                    })
                    db.session.commit()
                    current_app.logger.info("✅ Google token refreshed and saved.")
                except RefreshError as e:
                    current_app.logger.warning(f"Refresh failed: {e}")
                    return {
                        "error": "Google credentials expired or revoked. "
                                 "Please re‑authenticate via /start-auth."
                    }, 401
                except Exception as e:
                    current_app.logger.error(f"Unexpected refresh error: {e}")
                    return {
                        "error": "Token refresh failed. Please re‑authenticate."
                    }, 401
            
            elif ENV == "development":
                creds = run_oauth2flow(temp_credentials_file=temp_credentials_file)
            elif ENV == "production":
                print("ENV:", ENV)
                print("Decoded credentials dict:", credentials_dict)

                return {
                    "error": f"Missing or invalid credentials for user {user_id}. "
                             f"User must authenticate via /start-auth?user_id={user_id}"
                }, 401


        service = build(serviceName="calendar", version="v3", credentials=creds)
        event = {
            "summary":summary,
            "location":location,
            "description":description,
            "colorId":6,
            "start": {
                "dateTime":dateTime,
                "timeZone":"Africa/Lagos"
            },
            "end": {
                "dateTime":endDateTime,
                "timeZone":"Africa/Lagos"
            },
            "attendees":[
                {"email":email}
            ],
            "reminders": {
                "useDefault":False,
                "overrides":[
                    {"method":"email", "minutes":24 * 60},
                    {"method":"popup", "minutes":10}
                ]
            }
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        return({
            "message":"Event created successfully!",
            "eventLink":event.get("htmlLink")
        }), 201
    except HttpError as error:
        traceback.print_exc()
        print("An error occurred:", error)
        return({"error":str(error)}), 500

def run_oauth2flow(temp_credentials_file):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=temp_credentials_file, 
        scopes=SCOPES
        )
        # local server for dev.
    creds = flow.run_local_server(
        port=8000, 
        open_browser=True, 
        authorization_prompt_message="Please visit this URL to authorize access to your google calendar", 
        success_message="Authorization successful!, You may close this window.",
        access_type="offline",
        prompt="consent"
    )
    return creds
