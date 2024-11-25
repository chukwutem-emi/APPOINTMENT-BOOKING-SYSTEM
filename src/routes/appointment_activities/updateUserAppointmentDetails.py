from flask import request, jsonify
from flaskFile import app
from routes.authentication.accessToken import token_required
from tables.dbModels import Appointment, db, User
from sqlalchemy.exc import SQLAlchemyError as dbError
from sqlalchemy import text as t
from datetime import datetime


@app.route(rule="/update_user_appointment", methods=["PUT"])
@token_required
def update_user_appointment_details(current_user):
    try:
        Appointment()
        User()
        if not current_user:
            return jsonify({"appointment_update_not_allowed":"Unauthorized!. You can't perform this operation, login required. Please login!"}), 401
        
        data=request.get_json()
        if not data:
            return jsonify({"appointment_update_input_error":"Invalid input!"}), 400
        
        required_fields = ["first_name", "last_name", "gender", "user_phone_number", "address", "email_address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "appointment_time", "appointment_date"]
        for field in required_fields:
            if field not in data:
                return jsonify({"user_appointment_update_input_error":f"Missing required field:{field}"}), 400
            
        first_name = str(data["first_name"])
        last_name = str(data["last_name"])
        gender = str(data["gender"])
        user_phone_number = str(data["user_phone_number"])
        address = str(data["address"])
        email_address = str(data["email_address"])
        next_of_kin = str(data["next_of_kin"])
        next_of_kin_phone_number = str(data["next_of_kin_phone_number"])
        next_of_kin_address = str(data["next_of_kin_address"])
        appointment_description = str(data["appointment_description"])
        appointment_time_str = str(data["appointment_time"])
        appointment_time = datetime.strptime(appointment_time_str, "%H:%M").time()
        appointment_date_str = str(data["appointment_date"])
        appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()

        with db.engine.connect() as connection:
            get_user_info = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(get_user_info, {"public_id":current_user.public_id})
            user_dict = user_data.fetchone()
            user = user_dict._asdict()

            update_a_user_appointment_details = t("UPDATE appointment SET first_name=:first_name, last_name=:last_name, gender=:gender, user_phone_number=:user_phone_number, address=:address, email_address=:email_address, next_of_kin=:next_of_kin, next_of_kin_phone_number=:next_of_kin_phone_number, next_of_kin_address=:next_of_kin_address, appointment_description=:appointment_description, appointment_time=:appointment_time, appointment_date=:appointment_date WHERE user_id=:user_id")

            connection.execute(update_a_user_appointment_details, {"first_name":first_name, "last_name":last_name, "gender":gender, "user_phone_number":user_phone_number, "address":address, "email_address":email_address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "appointment_description":appointment_description, "appointment_time":appointment_time, "appointment_date":appointment_date, "user_id":user["id"]})
            connection.commit()

            return jsonify({"user_appointment_info":"User appointment details updated successfully!"}), 200
        
    except KeyError as k:
        return jsonify({"user_appointment_update_keyError":f"Missing data. A required key is missing.: {str(k)}"}), 400
    except ValueError as v:
        return jsonify({"user_appointment_update_valueError":f"There is an error in the value that you entered. Input error!.:{str(v)}"}), 400
    except dbError as d:
        return jsonify({"user_appointment_update_dbError":f"The server/database encountered an error. Please try again later.:{str(d)}"}), 500
    except Exception as e:
        return jsonify({"user_appointment_update_exc":f"An error has occurred during your user-appointment-update request. Please try again later!.:{str(e)}"}), 400
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")