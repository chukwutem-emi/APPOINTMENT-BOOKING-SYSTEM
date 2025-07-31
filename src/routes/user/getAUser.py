from routes.authentication.accessToken import token_required
from flask import jsonify, abort, request, make_response
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError


@token_required
def get_user(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"Unauthorized": "⚠️ You are not Authorized to perform this operation. please login!"}), 401
    try:
        user_data = {
            "username":current_user.username,
            "email_address":current_user.email_address,
            " public_id":current_user. public_id,
            "phone_number":current_user.phone_number,
            "admin":current_user.admin
        }
        if not user_data or len(user_data) == 0:
            return jsonify({"Not-Found": "User not found!"}), 404
        
        return jsonify({"user": user_data}), 200
    except SQLAlchemyError as dataBaseError:
        return jsonify({"getUser_dbError":f"Database Error:{str(dataBaseError)}"}), 500
    except Exception as Ex:
        return jsonify({"getUser_exc":f"An error has occurred during fetching your details!. Please try again later.:{str(Ex)}"}), 500
    





