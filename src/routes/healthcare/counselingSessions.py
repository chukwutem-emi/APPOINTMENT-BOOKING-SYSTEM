from flask import request, jsonify, redirect, current_app, make_response
import requests
from tables.dbModels import AppointmentTypes, db
from sqlalchemy import text as t
from routes.authentication.accessToken import token_required
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError as dbError
from datetime import datetime, timedelta
from routes.utils.constants import PAYSTACK_PAYMENT_API
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


@token_required
def counseling_session(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    current_app.logger.info("counseling session route called!")
    try:
        if not current_user:
            return({"counseling_error": "Unauthorized to carry out counseling appointment operation. Login required!"}), 401
        data = request.get_json()
        if not data:
            return jsonify({"counseling_data_error":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"counseling_input_error":f"Missing required field:{field}"}), 400
        first_name = str(data["first_name"])
        last_name = str(data["last_name"])
        gender = str(data["gender"])
        user_phone_number = str(data["user_phone_number"])
        address = str(data["address"])
        email_address = str(data["email_address"])
        next_of_kin = str(data["next_of_kin"])
        next_of_kin_phone_number = str(data["next_of_kin_phone_number"])
        next_of_kin_address = str(data["next_of_kin_address"])
        amount = float(data["amount"])
        appointment_description = str(data["appointment_description"])
        appointment_time_str = str(data["appointment_time"])
        appointment_time = datetime.strptime(appointment_time_str, "%H:%M").time()
        appointment_date_str = str(data["appointment_date"])
        appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()


        duration=60
        price=15000
        doctor="Dr. Samuel"
        hospital="ChemSten Hospital"
        location="40c, community road, off lasu-Isheri road, Obadore, lagos State"
        tel="07025347067"

        end_time = (datetime.combine(date=appointment_date, time=appointment_time) + timedelta(minutes=duration)).time()

        if not amount:
            return jsonify({"counseling_payment_required":f"Hi {first_name}, payment is require!"}), 402

        if amount < price:
            return jsonify({"counseling_payment_error":f"The minimum amount is:{price/1700:.2f}$."}), 403
        
        payload = {
            "email_address":email_address,
            "amount":int(amount * 100)
        }
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(url=PAYSTACK_PAYMENT_API, headers=headers, json=payload)
        response_data = response.json()
        if response_data["status"]:
            return jsonify({"counseling_response":response_data}), 200
        
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"counselingErrorMessage":"user not found!"}), 404
            user = user_data._asdict()
            user_id = user["id"]
           
            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, duration, price, doctor, location, tel, hospital, appointment_types, user_id, appointment_time, appointment_date, appointment_description, appointment_endTime
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :email_address, :next_of_kin, :next_of_kin_phone_number, :next_of_kin_address, :duration, :price, :doctor, :location, :tel, :hospital, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :appointment_endTime
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "duration":duration, "price":price, "doctor":doctor, "location":location, "tel":tel, "hospital":hospital, "appointment_types":AppointmentTypes.COUNSELING.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "appointment_endTime":end_time
                })
            connection.commit()
            subject = "ChemSten Hospital"
            body = f"Hi {last_name}!,\n\nCounseling appointment was booked successfully!,\nTime:{appointment_time}-{end_time},\nDate:{appointment_date},\nDuration:{duration}minutes,\n\nThanks for using our service,\nBest regard,\nChemSten Hospital Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            summary = f"This is an appointment for:\n{AppointmentTypes.COUNSELING.value}"
            dateTime = f"{appointment_date}T{appointment_time}+01:00"
            end_dateTime = f"{appointment_date}T{end_time}+01:00"
            # capturing the response from book_appointment:
            appointment_response, status_code = book_appointment(
                summary=summary, 
                location=location, 
                description=appointment_description, 
                dateTime=dateTime, 
                email=email_address,
                endDateTime=end_dateTime,
                user_id=user_id
                )
            if status_code == 401:
                return jsonify({
                    "error": "Google token invalid or expired. Re-authentication required.",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({
                    "counselingEventErr":"Failed to create google calendar event", 
                    "details":appointment_response
                    }), 500
            return jsonify({
                "Counseling":"☑️ Counseling appointment was booked successfully!",
                "googleCalendarLink":html_link
                }), 201
        
    except (KeyError, ValueError) as KvError:
        return jsonify({"Counseling_keyError":f"Invalid input!:{str(KvError)}"}), 400
    except Exception as e:
        return jsonify({"Counseling_Exc":f"An error occurred during your counseling booking appointment operation: {str(e)}"}), 500
    except dbError as d:
        return jsonify({"Counseling_DB_error":f"Database/server error: {str(d)}"}), 500
    
