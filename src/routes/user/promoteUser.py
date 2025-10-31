from flask import request, jsonify as J, make_response
from tables.dbModels import db
from sqlalchemy.exc import SQLAlchemyError
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from dotenv import load_dotenv
import os
from mail.sendMail import send_mail
load_dotenv()


@token_required
def promote_user(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user.role == "super-admin":
        return J({"Access_denied":"⚠️ You don't have the permission to carry out this request. Unauthorized!"}), 401
    try:
        data = request.get_json()
        required_field_for_promotion = ["username"]

        for field in required_field_for_promotion:
            if field not in data:
                return J({"promotion_requiredField":f"Missing required field!.:{field}"}), 400

        username = str(data["username"]).upper().strip()
        print(">>> RECEIVED USERNAME:", repr(username))
        admin = True
        user_role = "admin"
        
        with db.engine.connect() as connection:
            check_user_smt = t("SELECT * FROM user WHERE username=:username")
            user_smt = connection.execute(statement=check_user_smt, parameters={"username":username}).fetchone()
            if not user_smt:
                return J({"Promotion_error":"User not found or the user does not exist!"}), 404
            
            result = user_smt._asdict()
            userResult = result["admin"]
            email_address = result["email_address"]

            if userResult == True:
                return J({"AlreadyAdmin": "User is already an admin"}), 400
            
            promote_user_to_admin_user = t("UPDATE user SET admin=:admin, role=:role WHERE username=:username")
            connection.execute(statement=promote_user_to_admin_user, parameters={"admin":admin, "role":user_role, "username":username})
            connection.commit()

            subject = "Promotion"
            body = f"Hi @{email_address}!\n\nCongratulations!, you have been promoted to an admin-user,\n\nBest regard!,\nThe Team."
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            return J({"Promoted": "☑️ User has been Promoted to an Admin-user"}), 200
        
    except SQLAlchemyError as SQ:
        return J({"promotion_dbError":f"Database error. The server/database has encountered an error during the Promotion request: {str(SQ)}"}), 500

    except Exception as Exp:
        return J({"promotion_exc":f"An error has occurred from the Promotion request: {str(Exp)}"}), 500
        