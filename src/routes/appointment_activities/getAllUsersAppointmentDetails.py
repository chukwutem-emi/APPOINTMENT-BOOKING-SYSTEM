from flask import jsonify, request, make_response
from tables.dbModels import db
from sqlalchemy import text as t
from routes.authentication.accessToken import token_required
from sqlalchemy.exc import SQLAlchemyError as dbError
from datetime import datetime, timedelta

@token_required
def users_appointment_details(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user.admin:
        return jsonify({"admin_users_only":"Unauthorized!. You are not permitted to perform this request, it is meant for only admin users."}), 401
    try: 
        with db.engine.connect() as connection:
            get_all_users_appointment = t("SELECT * FROM appointment")
            appointments_data = connection.execute(get_all_users_appointment).fetchall()
            if len(appointments_data) == 0:
                return jsonify({"message":"The database is empty or it does not contain any appointment."}), 404
            appointments_list = []
            for appointment in appointments_data:
                if appointment not in appointments_list:
                    appointment_dict = appointment._asdict()
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
    
