import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
from routes.utils.constants import SCOPE
import base64
import json
from flask import current_app, jsonify
from tables.dbModels import User, db
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

def book_appointment(summary, location, description, dateTime, email, endDateTime, personnel_email):
    current_app.logger.info("book appointment function called!")
    try:
        credential = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
    except Exception as e:
        current_app.logger.error(f"FAILED to load google credentials. {e}")
        return jsonify({"message":"Internal server error: Failed to authenticate with google calender"}), 500
    
    service = build(serviceName="calendar", version="v3", credentials=credential)
    event_body = {
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
            {"email":email},
            {"email":personnel_email}
        ],
        "reminders": {
            "useDefault":False,
            "overrides":[
                {"method":"email", "minutes":24 * 60},
                {"method":"popup", "minutes":10}
            ]
        }
    }
    try:
        event = service.events().insert(calendarId="primary", body=event_body).execute()
    except Exception as E:
        current_app.logger.error(f"FAILED to create calendar event")
        return jsonify({"eventError": "Failed to create google calendar event"}), 500
    
    return({
        "message":"Event created successfully!",
        "eventLink":event.get("htmlLink")
    }), 201