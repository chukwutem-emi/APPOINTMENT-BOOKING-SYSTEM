from flaskFile import app
from flask import request, jsonify
import requests
from tables.dbModels import User, Appointment, AppointmentTypes, db
from sqlalchemy import text as t
from routes.authentication.accessToken import token_required
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError as dbError
from datetime import datetime
from routes.utils.constants import PAYSTACK_PAYMENT_API
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

@app.route(rule="/vaccination", methods=["POST"])
@token_required
def vaccination_session(current_user):
    try:
        User()
        Appointment()
        
        if not current_user:
            return({"vaccination_error": "Unauthorized to carry out vaccination appointment operation. Login required!"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"vaccination_data_error":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"vaccination_input_error":f"Missing required field:{field}"}), 400
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
        price=50000
        doctor="Dr. Solomon"
        hospital="ChemSten Hospital"
        location="40c, community road, off lasu-Isheri road, Obadore, lagos State"
        tel="07025347067"

        if not amount:
            return jsonify({"vaccination_payment_required":f"Hi {first_name}, payment is require!"}), 402

        if amount < price:
            return jsonify({"vaccination_payment_error":f"The minimum amount is:{price/1700:.2f}$."}), 403
        
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
            return jsonify({"vaccination_response":response_data}), 200
        
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"vaccinationErrorMessage":"user not found!"}), 404
            user = user_data._asdict()

            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, duration, price, doctor, location, tel, hospital, appointment_types, user_id, appointment_time, appointment_date, appointment_description
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :next_of_kin :email_address, :next_of_kin_phone_number, :next_of_kin_address, :duration, :price, :doctor, :location, :tel, :hospital, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "duration":duration, "price":price, "doctor":doctor, "location":location, "tel":tel, "hospital":hospital, "appointment_types":AppointmentTypes.VACCINATION.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description
                })
            connection.commit()

            subject = "ChemSten Hospital"
            body = f"Hi {last_name}!,\n\nVaccination appointment was booked successfully!,\n\ntime:{appointment_time},\ndate:{appointment_date},\nduration:{duration}minutes,\n\nThanks for using our service,\nBest regard,\nChemSten Hospital Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            summary = f"This is an appointment for:\n{AppointmentTypes.VACCINATION.value}"
            dateTime = f"{appointment_date}T{appointment_time}+01:00"
            # capturing the response from book_appointment:
            appointment_response, status_code = book_appointment(
                summary=summary, 
                location=location, 
                description=appointment_description, 
                dateTime=dateTime, 
                email=email_address
                )
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({
                    "consultationEventErr":"Failed to create google calendar event", 
                    "details":appointment_response
                    }), 500
            return jsonify({
                "vaccination":"Vaccination appointment was booked successfully!",
                "googleCalendarLink":html_link
                }), 201
        
    except (KeyError, ValueError) as KvError:
        return jsonify({"vaccination_kvError":f"Invalid input!:{str(KvError)}"}), 400
    except Exception as e:
        return jsonify({"vaccination_Exc":f"An error occurred during your vaccination booking appointment operation: {str(e)}"}), 500
    except dbError as d:
        return jsonify({"Vaccination_DB_error":f"Database/server error: {str(d)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")
