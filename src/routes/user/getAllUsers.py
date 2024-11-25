from flask import jsonify
from flaskFile import app
from tables.dbModels import db, User
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError 

@app.route(rule="/users", methods=["GET"])
@token_required
def get_users(current_user):
    try:
        User()
        if not current_user.admin:
            return jsonify({"Not_an_admin": "⚠️ You are not Authorized to perform this operation!. This operation is meant for Admin users only"}), 401
        with db.engine.connect() as connection:
            get_all_users = t("SELECT * FROM user")
            users=connection.execute(get_all_users)
            if users.rowcount == 0:
                return jsonify({"database_empty":"There are no records found in the database!."}), 404
            users_list = []
            for user in users:
                if user not in users_list:
                    users_dict = {
                        "username":user.username,
                        "public_id":user.public_id,
                        "email_address":user.email_address,
                        "phone_number":user.phone_number,
                        "admin":user.admin,
                        "created_at":user.created_at,
                        "updated_at":user.updated_at
                    }
                users_list.append(users_dict)
            return jsonify({"Users": users_list}), 200
        
    except SQLAlchemyError as dataBaseError:
        return jsonify({"getUsers_dbError":f"Database/server error: {str(dataBaseError)}"}), 500

    except Exception as E:
        return jsonify({"getUsers_exc":f"An error has occurred during the course of Your fetch-all Users operation. Please try again later, thank you!.:{E}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")