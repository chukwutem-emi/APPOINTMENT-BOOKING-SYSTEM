import requests
from flask import request, jsonify, redirect
from tables.dbModels import User, db, Appointment, AppointmentTypes
from routes.authentication.accessToken import token_required
from dotenv import load_dotenv
import os
from routes.utils.constants import PAYSTACK_PAYMENT_API
from sqlalchemy import text as t
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError as dbError
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

@token_required
def academic_advising(current_user):
    try:
        if not current_user:
            return({"Login_required": "Unauthorized!"}), 401
        data = request.get_json()
        if not data:
            return jsonify({"Err":"Invalid input"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]

        for field in required_fields:
            if field not in data:
                return jsonify({"academicAdv_fieldError":f"Missing data.:{field}"}), 400

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
        duration = 90
        price = 40000
        tutor = "Mr. Ebube Okoro"
        location = "40c, community road, off lasu-Isheri road, Obadore, lagos State"
        tel="07025347067"
        institution_name = "ChemSten University"

        end_time = (datetime.combine(date=appointment_date, time=appointment_time)+timedelta(minutes=duration)).time()
        
        if not amount:
            return jsonify({"Required":f"Hi {first_name}, payment is require!"}), 402

        if amount < price:
            return jsonify({"Payment_error":f"The minimum amount is:{price/1700:.2f}$."}), 403
        
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
            return jsonify({"payStack_response":response_data}), 200
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(get_the_login_user, {"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"message":"user not found!"}), 404
            user = user_data._asdict()
            user_id = user["id"]
            if not user or not user.get("google_token"):
                return redirect(f"/api/bookApp/start-Oauth?user_id={user_id}")

            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, duration, price, tutor, location, tel, institution_name, appointment_types, user_id, appointment_time, appointment_date, appointment_description, appointment_endTime
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :email_address, :next_of_kin,  :next_of_kin_phone_number, :next_of_kin_address, :duration, :price, :tutor, :location, :tel, :institution_name, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :appointment_endTime
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "duration":duration, "price":price, "tutor":tutor, "location":location, "tel":tel, "institution_name":institution_name, "appointment_types":AppointmentTypes.ACADEMIC_ADVISING.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "appointment_endTime":end_time
                })
            connection.commit()

            subject = "ChemSten University"
            body = f"Hi {last_name}!,\n\nYour academic advising appointment was booked successfully!,\ntime:{appointment_time},\ndate:{appointment_date},\nduration:{duration},\n\nThanks for using our service\nBest regard!\nChemSten University Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)
        
            summary = f"This is an appointment for: {AppointmentTypes.ACADEMIC_ADVISING.value}"
            dateTime = f"{appointment_date}T{appointment_time}+01:00"
            endDateTime = f"{appointment_date}T{end_time}+01:00"
            # Capturing response from book_appointment
            appointment_response, status_code = book_appointment(
                summary=summary, 
                location=location, 
                description=appointment_description, 
                dateTime=dateTime, 
                email=email_address,
                endDateTime=endDateTime,
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
                return jsonify({"academicErr":"Failed to create google calender event",
                                "details":appointment_response
                                }), 500

            return jsonify({"Academic_advising":"☑️ Academic advising appointment was booked successfully!",
                            "googleCalenderEvent":html_link
                            }), 201
    except (KeyError, ValueError) as kvError:
        return jsonify({"academicAdv_kvError":f"Invalid input!.:{str(kvError)}"}), 400
    except dbError as d:
       return jsonify({"academicAdv_dbError":f"Database/server error.:{str(d)}"}), 500
    except Exception as e:
        return jsonify({"academicAdv_exc":f"An error occurred: {str(e)}"}), 500
    