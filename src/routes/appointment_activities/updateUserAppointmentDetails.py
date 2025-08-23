from flask import request, jsonify, make_response
from routes.authentication.accessToken import token_required
from tables.dbModels import db
from sqlalchemy.exc import SQLAlchemyError as dbError
from sqlalchemy import text as t
from datetime import datetime
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment

@token_required
def update_user_appointment_details(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"appointment_update_not_allowed":"Unauthorized!. You can't perform this operation, login required. Please login!"}), 401
    try:     
        data=request.get_json()
        if not data:
            return jsonify({"appointment_update_input_error":"Invalid input!"}), 400
        
        required_fields = ["gender", "address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "appointment_time", "appointment_date", "appointment_description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"user_appointment_update_input_error":f"Missing required field:{field}"}), 400
            
        gender                   = str(data["gender"])
        address                  = str(data["address"])
        next_of_kin              = str(data["next_of_kin"])
        next_of_kin_phone_number = str(data["next_of_kin_phone_number"])
        next_of_kin_address      = str(data["next_of_kin_address"])
        appointment_description  = str(data["appointment_description"])
        appointment_time_str     = str(data["appointment_time"])
        appointment_time         = datetime.strptime(appointment_time_str, "%H:%M").time()
        appointment_date_str     = str(data["appointment_date"])
        appointment_date         = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()

        with db.engine.connect() as connection:
            get_user_info = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(get_user_info, {"public_id":current_user.public_id})
            user_dict = user_data.fetchone()
            user = user_dict._asdict()

            user_id       = user["id"]
            email_address = user["email_address"]
            phone_number  = user["phone_number"]
            username      = user["username"]

            update_a_user_appointment_details = t("UPDATE appointment SET gender=:gender, user_phone_number=:user_phone_number, address=:address, next_of_kin=:next_of_kin, next_of_kin_phone_number=:next_of_kin_phone_number, next_of_kin_address=:next_of_kin_address, appointment_description=:appointment_description, appointment_time=:appointment_time, appointment_date=:appointment_date, user_id=:user_id WHERE user_id=:user_id")

            connection.execute(update_a_user_appointment_details, {"gender":gender, "user_phone_number":phone_number, "address":address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "appointment_description":appointment_description, "appointment_time":appointment_time, "appointment_date":appointment_date, "user_id":user_id})
            connection.commit()

            subject = "Appointment update!"
            body = f"HI {username}!,\n\nYour appointment details was updated successfully!,\nTime:{appointment_time},\nDate:{appointment_date},\n\nThanks for using our service\nBest regard!\nThe Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            return jsonify({"user_appointment_info":"☑️ User appointment details updated successfully!"}), 200
        
    except (KeyError, ValueError) as kv:
        return jsonify({"user_appointment_update_keyValueError":f"Invalid Input!: {str(kv)}"}), 400
    except dbError as d:
        return jsonify({"user_appointment_update_dbError":f"The server/database encountered an error. Please try again later.:{str(d)}"}), 500
    except Exception as e:
        return jsonify({"user_appointment_update_exc":f"An error has occurred during your user-appointment-update request. Please try again later!.:{str(e)}"}), 500
    