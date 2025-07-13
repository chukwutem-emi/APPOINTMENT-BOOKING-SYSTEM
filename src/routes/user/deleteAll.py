from flask import jsonify, request, make_response
from tables.dbModels import db
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError 
from routes.authentication.accessToken import token_required


@token_required
def delete_all_users(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    try:
        if not current_user.admin:
            return jsonify({"permission_denied": "⚠️ Hey!, keep off. You are not allowed!."}), 403
        
        with db.engine.connect() as connection:
            delete_all_users_data = t("DELETE FROM user")
            users=connection.execute(delete_all_users_data)
            if users.rowcount == 0:
                return jsonify({"empty_database":"The database has no users. Database is empty!"}), 404
            connection.commit()
            return jsonify({"all_users_deleted": "☑️ All users has been deleted successfully!"}), 200
        
    except Exception as e:
        return jsonify({"deleting_all_user_exc":f"An error has occurred during your request to delete-all-user-information from the database:{str(e)}"}), 400
    except SQLAlchemyError as s:
        return jsonify({"delete_all_s=user_dbError":f"The server encountered an error. Please try again later!.:{str(s)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")