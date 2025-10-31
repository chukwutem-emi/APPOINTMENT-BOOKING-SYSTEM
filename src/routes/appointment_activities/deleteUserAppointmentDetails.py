from flask import request, jsonify, make_response
from tables.dbModels import db
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError


@token_required
def delete_user_appointment_details(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user.admin:
        return jsonify({"Unauthorized_user":"You are not authorized to perform this operation. Access denied!"}), 401
    
    try:
        data =  request.get_json()
        username = str(data["username"]).upper().strip()

        with db.engine.connect() as connection:
            delete_a_user_appointment_details = t("DELETE FROM appointment WHERE username=:username")
            delete_app = connection.execute(delete_a_user_appointment_details, {"username":username})
            if delete_app.rowcount == 0:
                return jsonify({"message":"The Appointment does not exist or the appointment has already been deleted from the database"}), 404
            connection.commit()

            return jsonify({"user_appointment_details":"User appointment details was deleted successfully!"}), 200
    
    except SQLAlchemyError as s:
        return jsonify({"user_db_appointment_details":f"The database/server encountered an error:{str(s)}"}), 500
    except Exception as e:
        return jsonify({"user_appointment_details_exc":f"An error has occurred during deleting the user-appointment-details:{str(e)}"}), 400
    