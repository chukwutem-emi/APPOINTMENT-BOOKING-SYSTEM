from flask import jsonify, request, make_response
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError as dbError
from tables.dbModels import db 
from routes.authentication.accessToken import token_required
from datetime import timedelta, datetime

@token_required
def a_user_appointment_details(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"get_user_appointment_denied":"Unauthorized!. You are not allowed to perform this operation. Please login"}), 401
    try:      
        with db.engine.connect() as connection:
            get_a_user_appointment_details = t("SELECT * FROM appointment WHERE user_id=:user_id")

            user_appointments = connection.execute(statement=get_a_user_appointment_details, parameters={"user_id":current_user.id}).fetchone()
            if not user_appointments:
                return jsonify({"user_appointment_not found":"The user appointment details that You are trying to access is not found!"}), 404
            
            # clean the row
            appointment_dict = {}
            for key, value in user_appointments._mapping.items():
                # Skip null values
                if value is None:
                    continue   
                elif isinstance(value, timedelta):
                    appointment_dict[key] = str(value)
                elif isinstance(value, datetime):
                    appointment_dict[key] = value.isoformat()
                else:
                    appointment_dict[key] = value
            return jsonify({"user_appointments":appointment_dict}), 200
        
    except dbError as d:
        return jsonify({"a_user_appointment_dbError":f"The server/database encountered an error. Please try again later!:{str(d)}"}), 500
    except Exception as e:
        return jsonify({"a_user_appointment_exc":f"An error has occurred during your fetch a_user_appointment_details request. Please try again later!:{str(e)}"}), 400
    