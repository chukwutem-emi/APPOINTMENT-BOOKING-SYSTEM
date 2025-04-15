from flask import jsonify
from flaskFile import app
from tables.dbModels import db
from sqlalchemy import text as t
from routes.authentication.accessToken import token_required
from sqlalchemy.exc import SQLAlchemyError as dbError
from datetime import datetime, timedelta

@app.route(rule="/users_appointment", methods=["GET"])
@token_required
def users_appointment_details(current_user):
    try:
        if not current_user.admin:
            return jsonify({"admin_users_only":"Unauthorized!. You are not permitted to perform this request, it is meant for only admin users."}), 401
        
        with db.engine.connect() as connection:
            get_all_users_appointment = t("SELECT * FROM appointment")
            appointments_data = connection.execute(get_all_users_appointment).fetchall()
            appointments_list = []
            for appointment in appointments_data:
                if appointment not in appointments_list:
                    appointment_dict = {
                     "user_id":appointment.user_id,
                     "id":appointment.id,
                     "first_name":appointment.first_name,
                     "last_name":appointment.last_name,
                     "gender":appointment.gender,
                     "user_phone_number":appointment.user_phone_number,
                     "address":appointment.address,
                     "email_address":appointment.email_address,
                     "next_of_kin":appointment.next_of_kin,
                     "next_of_kin_phone_number":appointment.next_of_kin_phone_number,
                     "next_of_kin_address":appointment.next_of_kin_address,
                     "duration":appointment.duration,
                     "price":appointment.price,
                     "doctor":appointment.doctor,
                     "hospital":appointment.hospital,
                     "location":appointment.location,
                     "tel":appointment.tel,
                     "consultant_name":appointment.consultant_name,
                     "organization_name":appointment.organization_name,
                     "organization_address":appointment.organization_address,
                     "tutor":appointment.tutor,
                     "institution_name":appointment.institution_name,
                     "phone_repair_price":appointment.phone_repair_price,
                     "laptop_repair_price":appointment.laptop_repair_price,
                     "appointment_types":appointment.appointment_types,
                     "appointment_time":appointment.appointment_time,
                     "appointment_date":appointment.appointment_date,
                     "appointment_description":appointment.appointment_description
                    }
                cleaned_all_users_appointment_row = {}
                for key, value in appointment_dict.items():
                    # Skip null value
                    if value is None:
                        continue
                    elif isinstance(value, timedelta):
                        cleaned_all_users_appointment_row[key] = str(value)
                    elif isinstance(value, datetime):
                        cleaned_all_users_appointment_row[key] = value.isoformat()
                    else:
                        cleaned_all_users_appointment_row[key] = value
                appointments_list.append(cleaned_all_users_appointment_row)

            return jsonify({"All_appointments":appointments_list}), 200

    except dbError as d:
        return jsonify({"all_appointment_dbError":f"The database/server encountered an error. Please try again later!:{str(d)}"}), 500
    except Exception as E:
        return jsonify({"all_appointment_exc":f"An error has occurred during your request. Please try again later!:{str(E)}"}), 400
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!") 
