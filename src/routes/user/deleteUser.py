from flask import jsonify as J, make_response, request
from tables.dbModels import db
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError


@token_required
def delete_user(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user.admin:
        return J({"Not_permitted":"⚠️ You are Unauthorized to make this request"}), 401
    try:  
        with db.engine.connect() as connection:
            delete_user_info = t("DELETE FROM user WHERE public_id=:public_id")
            user_details = connection.execute(statement=delete_user_info, parameters={"public_id":current_user.public_id})
            user = user_details

            if user.rowcount ==0 :
                return J({"Empty":"User details are null(empty) or user not found!"}), 404
            connection.commit()
            return J({"Deleted":"☑️ User information has been deleted from the database successfully!"}), 200
        
    except SQLAlchemyError as Error:
        return J({"deleteUser_dbError":f"Database/server error.:{str(Error)}"}), 500
    except Exception as Exp:
        return J({"deleteUser_exc":f"An error occurred!.:{str(Exp)}"}), 500
        