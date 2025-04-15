from flask import request, jsonify as J
from flaskFile import app
from tables.dbModels import db
from sqlalchemy.exc import SQLAlchemyError
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from dotenv import load_dotenv
import os
from mail.sendMail import send_mail
load_dotenv()

access_code = os.getenv("ACCESS_CODE")

@app.route(rule="/promote", methods=["PUT"])
@token_required
def promote_user(current_user):
    try:
        if not current_user:
            return J({"Access_denied":"⚠️ You don't have the permission to carry out this request. Unauthorized!"}), 401
        
        data = request.get_json()
        required_field_for_promotion = ["email_address", "code"]

        for field in required_field_for_promotion:
            if field not in data:
                return J({"promotion_requiredField":f"Missing required field!.:{field}"}), 400

        email_address = str(data["email_address"])
        admin = True
        
        provided_code = str(data["code"])
        if provided_code != access_code:
            return({"Code_Error":"⚠️ Access denied!"}), 401

        with db.engine.connect() as connection:
            promote_user_to_admin_user = t("UPDATE user SET admin=:admin WHERE email_address=:email_address")
            user_promotion = connection.execute(statement=promote_user_to_admin_user, parameters={"admin":admin, "email_address":email_address})

            user = user_promotion
            if user.rowcount == 0:
                return J({"Promotion_error":"User not found or the user does not exist!"}), 404
            
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
    finally:
        if connection:
            connection.close()
            print("The database connection as been closed!")
        