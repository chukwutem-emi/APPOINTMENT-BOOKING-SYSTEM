import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from routes.utils.constants import SCOPE
from flask import jsonify
import json
from flask import current_app
from tables.dbModels import User, db


def book_appointment(summary, location, description, dateTime, email, endDateTime, personnel_email, user_id):
    current_app.logger.info("book appointment function called!")
    # 1. Get the user's saved token from DB
    user = User.query.get(user_id)
    if not user or not user.google_token:
        return jsonify({
                    "error": "User not authenticated with google",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401
    try:
        token_data = json.loads(user.google_token)
        creds = Credentials.from_authorized_user_info(token_data)

        if creds or (creds.expired and not creds.refresh_token):
            return jsonify({
                    "error": "Google token invalid or expired. Re-authentication required.",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            user.google_token = creds.to_json()
            db.session.commit()

    except Exception as e:
        current_app.logger.error(f"Failed to load user credentials.{str(e)}")
        return jsonify({
                    "error": "Google token invalid or expired. Re-authentication required.",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401
    
    
    # 2. Build the Calendar API client
    service = build(serviceName="calendar", version="v3", credentials=creds)

    # 3. Create the event body
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
    # 4. Insert event into user's primary calendar
    try:
        event = service.events().insert(calendarId="primary", body=event_body).execute()
    except Exception as E:
        current_app.logger.error(f"FAILED to create calendar event")
        return{"eventError": f"Failed to create google calendar event{str(E)}"}, 500
    
    return{
        "message":"Event created successfully!",
        "eventLink":event.get("htmlLink")
    }, 201