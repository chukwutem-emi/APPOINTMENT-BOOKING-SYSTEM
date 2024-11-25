from flask import jsonify
from flaskFile import app
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError as dbError
from tables.dbModels import Appointment, db
from routes.authentication.accessToken import token_required


@app.route(rule="/user_appointment", methods=["GET"])
@token_required
def a_user_appointment_details(current_user):
    try:
        Appointment()

        if not current_user:
            return jsonify({"get_user_appointment_denied":"Unauthorized!. You are not allowed to perform this operation. Please login"}), 401
        
        with db.engine.connect() as connection:
            get_a_user_appointment_details = t("SELECT * FROM appointment WHERE user_id=:user_id")

            user_data = connection.execute(statement=get_a_user_appointment_details, parameters={"user_id":current_user.id})
            user = user_data.fetchall()
            if not user:
                return jsonify({"user_appointment_not found":"The user appointment details that You are trying to access is not found!"}), 404
            appointment_list = []
            for appointment in user:
                if appointment not in (None, "") not in appointment_list:
                    appointment_list.append(appointment._asdict())
            return jsonify(appointment_list), 200
        
    except dbError as d:
        return jsonify({"a_user_appointment_dbError":f"The server/database encountered an error. Please try again later!:{str(d)}"}), 500
    except Exception as e:
        return jsonify({"a_user_appointment_exc":f"An error has occurred during your fetch a_user_appointment_details request. Please try again later!:{str(e)}"}), 400
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")