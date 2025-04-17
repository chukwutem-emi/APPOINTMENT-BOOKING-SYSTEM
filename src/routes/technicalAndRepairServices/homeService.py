from flask import request, jsonify
from routes.authentication.accessToken import token_required
from tables.dbModels import db, AppointmentTypes
from datetime import datetime, timedelta
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError as dbError
import requests
import os
from dotenv import load_dotenv
from routes.utils.constants import PAYSTACK_PAYMENT_API
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


@token_required
def home_service(current_user):
    try:
        if not current_user:
            return jsonify({"home_service_error": "Unauthorized to carry out home service appointment operation. Login required!"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"home_service_data_error":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]

        for field in required_fields:
            if field not in data:
                return jsonify({"home_service_input_error":f"Missing required field:{field}"}), 400

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

        phone_repair_price="It depends on the type of the faults/damages"
        laptop_repair_price="It depends on the type of the faults/damages"
        organization_name="ChemSten Electronics"
        organization_address="40c, community road, off lasu-Isheri road, Obadore, lagos State"
        tel="07025347067"
        price = 80000
        duration = 240

        end_time = (datetime.combine(date=appointment_date, time=appointment_time) + timedelta(minutes=duration)).time()

        if not amount:
            return jsonify({"home_service_payment_required":f"Hi {first_name}, payment is require!"}), 402

        if amount < price:
            return jsonify({"home_service_payment_error":f"The minimum amount is:{price/1700:.2f}$."}), 403
        
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
            return jsonify({"home_service_response": response_data}), 200
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"homeServiceErrorMessage":"user not found!"}), 404
            user = user_data._asdict()

            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, phone_repair_price, price, laptop_repair_price, organization_address, tel, organization_name, appointment_types, user_id, appointment_time, appointment_date, appointment_description, duration, appointment_endTime
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :email_address, :next_of_kin,  :next_of_kin_phone_number, :next_of_kin_address, :phone_repair_price, :price, :laptop_repair_price, :organization_address, :tel, :organization_name, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :duration, :appointment_endTime
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "phone_repair_price":phone_repair_price, "price":price, "laptop_repair_price":laptop_repair_price, "organization_address":organization_address, "tel":tel, "organization_name":organization_name, "appointment_types":AppointmentTypes.HOME_SERVICES.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "duration":duration, "appointment_endTime":end_time
                })
            connection.commit()

            subject = "ChemSten Electronics"
            body = f"Hi {last_name}!,\n\nHome service appointment was booked successfully!,\ntime:{appointment_time},\ndate:{appointment_date},\n\nThanks for using our service,\nBest regard,\nChemSten Electronics Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            summary = f"This is an appointment for:\n{AppointmentTypes.ELECTRONICS_REPAIR.value}"
            dateTime = f"{appointment_date}T{appointment_time}+01:00"
            endDateTime = f"{appointment_date}T{end_time}+01:00"
            # capturing the response from book_appointment:
            appointment_response, status_code = book_appointment(
                summary=summary, 
                location=organization_address, 
                description=appointment_description, 
                dateTime=dateTime, 
                email=email_address,
                endDateTime=endDateTime
                )
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({"HomeServiceErr": "Failed to create google calender event",
                        "Details":appointment_response
                        }), 500

            return jsonify({"home_service":"☑️ Home service appointment was booked successfully!",
                            "googleCalenderEvent":html_link
                            }), 201

    except (KeyError, ValueError) as KvError:
        return jsonify({"home_service_kvError":f"Invalid input!:{str(KvError)}"}), 400
    except Exception as e:
        return jsonify({"home_service_Exc":f"An error occurred during your home service booking appointment operation: {str(e)}"}), 500
    except dbError as d:
        return jsonify({"home_service_DB_error":f"Database/server error: {str(d)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")