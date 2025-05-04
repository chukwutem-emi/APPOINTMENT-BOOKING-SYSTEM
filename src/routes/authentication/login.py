from werkzeug.security import check_password_hash
import uuid
from flask import jsonify, request, current_app
from tables.dbModels import db
from sqlalchemy import text as t
import jwt
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from mail.sendMail import send_mail

load_dotenv()



def sign_in():
    try:
        data = request.get_json()
        if not data or not data.get("email_address") or not data.get("password"):
            return jsonify({"invalid":"Invalid input"}), 400
        required_fields=["email_address", "password"]

        for field in required_fields:
            if field not in data:
                return jsonify({"login_fieldError":f"Missing require field.:{field}"}), 400
        email_address=str(data["email_address"])
        password=str(data["password"])

        with db.engine.connect() as connection:
            user_login=t("SELECT * FROM user WHERE email_address=:email_address")
            user_info=connection.execute(statement=user_login, parameters={"email_address":email_address})
            user=user_info.first()

            print("Password type:", type(user["password"]), "Value:", user["password"])
            # password_hashed=user["password"]
            # public_id=user["public_id"]
            # username=user["username"]

            if not user or not check_password_hash(user.password, password):
                return jsonify({"verification":"We could not verify your details!. Please check your input or signup if you haven't registered"}), 400
            token=jwt.encode({"public_id":user.public_id, "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(minutes=60)}, current_app.config["SECRET_KEY"])

            subject = "Login Alert!"
            body = f"Hi @{user.username}, You just signed-in into your account!.\n\nPlease if you are not the one that signed-in,\nthen contact-us at: chukwutememi@gmail.com,\n\nBest regard!\nThe Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver) 

            return({"Login_Verification":"☑️ Successfully Logged-In", "Token":token}), 200
            
    except (KeyError, ValueError)as kvError:
        return jsonify({"login_kvError":f"Invalid input!.:{str(kvError)}"}), 400
    except SQLAlchemyError as databaseError:
        return jsonify({"login_dbError":f"Database/server error.:{str(databaseError)}"}), 500
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"login_exc":f"An error has occurred!.:{str(e)}"}), 500
    
            