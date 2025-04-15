from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError as dbError
from flaskFile import app
from tables.dbModels import User, Appointment, AppointmentTypes, db
import requests
from routes.authentication.accessToken import token_required
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import text as t
from routes.utils.constants import PAYSTACK_PAYMENT_API
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

@app.route(rule="/career", methods=["POST"])
@token_required
def career_counseling(current_user):
    try:
        if not current_user:
            return jsonify({"Msg": "You are not permitted to perform this operation without login. Login required!"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"Data":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]

        for field in required_fields:
            if field not in data:
                return jsonify({"careerCounseling_fieldError":f"Missing required field.:{field}"}), 400

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
        tutor = "Mrs. Cynthia Nwaokolo"
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
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"careerErrorMessage":"user not found!"}), 404
            user = user_data._asdict()

            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, duration, price, tutor, location, tel, institution_name, appointment_types, user_id, appointment_time, appointment_date, appointment_description, appointment_endTime
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :email_address, :next_of_kin,  :next_of_kin_phone_number, :next_of_kin_address, :duration, :price, :tutor, :location, :tel, :institution_name, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :appointment_endTime
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "duration":duration, "price":price, "tutor":tutor, "location":location, "tel":tel, "institution_name":institution_name, "appointment_types":AppointmentTypes.CAREER_COUNSELING.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "appointment_endTime":end_time
                })
            connection.commit()
            subject = "ChemSten University"
            body = f"Hi {last_name}!,\n\nCareer counseling appointment was booked successfully!,\ntime:{appointment_time},\ndate:{appointment_date},\nduration:{duration},\n\nThanks for using our service,\nBest regard,\nChemSten University Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            summary = f"This is an appointment for: \n{AppointmentTypes.CAREER_COUNSELING.value}"
            dateTime = f"{appointment_date}T{appointment_time}+01:00"
            endDateTime = f"{appointment_date}T{end_time}+01:00"
            # capturing the response from book_appointment
            appointment_response, status_code = book_appointment(
                summary=summary,
                location=location,
                description=appointment_description,
                dateTime=dateTime,
                email=email_address,
                endDateTime=endDateTime
            )
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({"careerErr":"Failed to create calender event"}), 500

            return jsonify({"Career_counseling":"☑️ Career counseling appointment was booked successfully!",
                            "googleCalenderEvent":html_link
                            }), 201
    except (KeyError, ValueError) as kvError:
        return jsonify({"careerCounseling_kvError":f"Invalid input!.:{str(kvError)}"}), 400
    except dbError as d:
        return jsonify({"careerCounseling_dbError":f"Database/server error: {str(d)}"}), 500
    except Exception as E:
        return jsonify({"careerCounseling_exc": f"An error occurred: {str(E)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")