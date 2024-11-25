from flask import request, jsonify
from flaskFile import app
from routes.authentication.accessToken import token_required
from tables.dbModels import db, User, Appointment, AppointmentTypes
from datetime import datetime
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError as dbError
import requests
import os
from dotenv import load_dotenv
from routes.utils.constants import PAYSTACK_PAYMENT_API
from mail.sendMail import send_mail
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")



@app.route(rule="/electrical", methods=["POST"])
@token_required
def electrical_repair(current_user):
    try:
        User()
        Appointment()

        if not current_user:
            return jsonify({"electrical_repair_error": "Unauthorized to carry out electrical repair appointment operation. Login required!"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"electrical_repair_data_error":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "amount", "appointment_time", "appointment_date"]

        for field in required_fields:
            if field not in data:
                return jsonify({"electrical_repair_input_error":f"Missing required field:{field}"}), 400

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

        if not amount:
            return jsonify({"electrical_repair_payment_required":f"Hi {first_name}, payment is require!"}), 402

        if amount < price:
            return jsonify({"electrical_repair_payment_error":f"The minimum amount is:{price/1700:.2f}$."}), 403
        
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
            return jsonify({"electrical_repair_response": response_data}), 200
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if not user_data:
                return jsonify({"electricalRepairErrorMessage":"user not found!"}), 404
            user = user_data._asdict()

            user_appointment = t("""
                INSERT INTO appointment(
                    first_name, last_name, gender, user_phone_number, address, email_address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, phone_repair_price, price, laptop_repair_price, organization_address, tel, organization_name, appointment_types, user_id, appointment_time, appointment_date, appointment_description
                    ) VALUES(
                    :first_name, :last_name, :gender, :user_phone_number, :address, :next_of_kin :email_address, :next_of_kin_phone_number, :next_of_kin_address, :phone_repair_price, :price, :laptop_repair_price, :organization_address, :tel, :organization_name, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "phone_repair_price":phone_repair_price, "price":price, "laptop_repair_price":laptop_repair_price, "organization_address":organization_address, "tel":tel, "organization_name":organization_name, "appointment_types":AppointmentTypes.ELECTRONICS_REPAIR.value, "user_id":user["id"], "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description
                })
            connection.commit()

            subject = "ChemSten Electronics"
            body = f"Hi {last_name}!,\n\nElectronics repair appointment was booked successfully!,\ntime:{appointment_time},\ndate:{appointment_date},\n\nThanks for using our service,\nBest regard,\nChemSten Electrical's Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            return jsonify({"electronics_repair":"Electrical repair appointment was booked successfully!"}), 200

    except (KeyError, ValueError) as KvError:
        return jsonify({"electrical_repair_kvError":f"Invalid input!:{str(KvError)}"}), 400
    except Exception as e:
        return jsonify({"electrical_repair_Exc":f"An error occurred during your electrical repair booking appointment operation: {str(e)}"}), 500
    except dbError as d:
        return jsonify({"electrical_repair_DB_error":f"Database/server error: {str(d)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")