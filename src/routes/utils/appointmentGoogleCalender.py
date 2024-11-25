import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from flaskFile import app
from .constants import SCOPE
from .startOauth import start_oauth
from .oauth2Callback import oauth2callback
load_dotenv()
ENV = os.getenv("ENV", "development")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
print("secret:", GOOGLE_CREDENTIALS_JSON)

SCOPES = [SCOPE]
if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON in environment variables")

def book_appointment(summary, location, description, dateTime, email, endDateTime):
    creds = None
    token_path = os.path.join(os.getcwd(), f"token_{ENV}.json")
    temp_credentials_file = None
    try:
        # Write the credentials from the environment variable to a temporary file
        temp_credentials_file = "temp_credentials.json"
        with open(temp_credentials_file, "w") as temp_file:
            temp_file.write(GOOGLE_CREDENTIALS_JSON)

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=temp_credentials_file, 
                    scopes=SCOPES
                    )
                if ENV == "development":
                    # local server for dev.
                    creds = flow.run_local_server(
                        port=8000, 
                        open_browser=True, 
                        authorization_prompt_message="Please visit this URL to authorize access to your google calendar", 
                        success_message="Authorization successful!, You may close this window.",
                        access_type="offline",
                        prompt="consent"
                    )
                elif ENV == "production":
                    start_oauth()
                    oauth2callback(json_file=token_path)

            with open(token_path, "w") as token:
                token.write(creds.to_json())

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
        print("An error occurred:", error)
        return({"error":str(error)}), 500
    finally:
        if temp_credentials_file and os.path.exists(temp_credentials_file):
            os.remove(temp_credentials_file)