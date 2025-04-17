from flask import request, jsonify as J
from tables.dbModels import db
from werkzeug.security import generate_password_hash
from routes.authentication.accessToken import token_required
from sqlalchemy import text as t
from sqlalchemy.exc import  SQLAlchemyError
from mail.sendMail import send_mail

@token_required
def update_user(current_user):
    try:
        if not current_user:
            return({"Request Error": "⚠️ You are not Authorized to carry out this task. Please you have to login for verification, thank you!"}), 401
        
        data = request.get_json()
        if not data:
            return J({"update_dataError":"Invalid Input!"}), 400
            
        required_fields_for_update = ["username", "password", "email_address", "phone_number"]

        for field in required_fields_for_update:
            if field not in data:
                return J({"update_fieldError":f"Missing required field: {field}"}), 400

        hashed_password = generate_password_hash(password=data["password"], method="pbkdf2:sha256:600000")
        username = str(data["username"]).upper()
        password = hashed_password
        email_address = str(data["email_address"])
        phone_number = str(data["phone_number"])

        with db.engine.connect() as connection:
            update_a_user = t("""
                UPDATE user SET username=:username, 
                password=:password, email_address=:email_address, 
                phone_number=:phone_number 
                WHERE public_id=:public_id
            """)

            user=connection.execute(statement=update_a_user, parameters={
                "username":username, "password":password, "email_address":email_address, "phone_number":phone_number, "public_id":current_user.public_id})

            user_data = user
            if user_data is None:
                return J({"UserData_Not_Found":"Your details is not found in the database"}), 404
            connection.commit()
            
            subject = "ChemSten Appointment-Booking-System Update notification!"
            body = f"Hi {username}!,\n\nYour details has been uploaded and updated successfully as follows:\nUsername:{username},\nPhone-number:{phone_number},\nEmail-address:{email_address},\nPassword:{password},\n\nBest regard!,\nThe Team."
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            return J({"Updated": "☑️ Your details has been uploaded and updated successfully!"}), 200
        
    except (KeyError, ValueError) as kvError:
        return J({"update_kvError":f"Invalid input!.:{str(kvError)}"}), 400
    except SQLAlchemyError as dbError:
        return J({"update_dbError":f"Database Error. The database encountered an error: {str(dbError)}"}), 500
    except Exception as E:
        return J({"update_exc":f"An error has occurred during the course of Your update. please try again later!: {str(E)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")
        

