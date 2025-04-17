from flask import request, jsonify
from tables.dbModels import db
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError


@token_required
def delete_user_appointment_details(current_user):
    try:
        if not current_user.admin:
            return jsonify({"Unauthorized_user":"You are not authorized to perform this operation. Access denied!"}), 401
        with db.engine.connect() as connection:
            delete_a_user_appointment_details = t("DELETE FROM appointment WHERE user_id=:user_id")
            connection.execute(delete_a_user_appointment_details, {"user_id":current_user.id})
            connection.commit()

            return jsonify({"user_appointment_details":"User appointment details was deleted successfully!"}), 200
    
    except SQLAlchemyError as s:
        return jsonify({"user_db_appointment_details":f"The database/server encountered an error:{str(s)}"}), 500
    except Exception as e:
        return jsonify({"user_appointment_details_exc":f"An error has occurred during deleting the user-appointment-details:{str(e)}"}), 400
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")