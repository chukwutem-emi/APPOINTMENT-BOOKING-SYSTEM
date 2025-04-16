from flask import jsonify, request
from werkzeug.security import generate_password_hash
from src.tables.dbModels import db, User
import uuid
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError
from src.flaskFile import app
from src.mail.sendMail import send_mail


@app.route("/register", methods=["POST"])
def sign_up():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"registration_dataError":f"Invalid input.:{data}"}), 400
        required_fields=["username", "password", "email_address", "phone_number"]
        for field in required_fields:
            if field not in data:
                return jsonify({"registration_fieldsError":f"Missing required field.:{field}"}), 400
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256:600000")
        password=hashed_password
        username=str(data["username"]).upper()
        email_address=str(data["email_address"])
        phone_number=str(data["phone_number"])
        public_id=str(uuid.uuid4())
        admin=False
        with db.engine.connect() as connection:
            create_user=t("""
                INSERT INTO user(
                          password, username, email_address, phone_number, public_id, admin
                          ) VALUES(
                          :password, :username, :email_address, :phone_number, :public_id, :admin)
            """)

            connection.execute(statement=create_user, parameters={
                "password":password, "username":username, "email_address":email_address, "phone_number":phone_number, "public_id":public_id, "admin":admin
                })
            connection.commit()
            subject = "Welcome to Our Service"
            body = f"Hi {username}!,\n\nThank You for registering with us!\n\nBest regard,\nThe Team"
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)
            
            return jsonify({"success": "☑️ User created and uploaded successfully!"}), 201
    except (KeyError, ValueError) as kvError:
        return jsonify({"registration_kvError":f"Invalid inputs!.:{str(kvError)}"}), 400
    except SQLAlchemyError as dataBaseError:
        return jsonify({"registration_serverError":f"Database/server error.:{str(dataBaseError)}"}), 500
    except Exception as e:
        return jsonify({"registration_exc":f"An Unexpected error has occurred during the course of your registration.:{str(e)}"}), 500
    finally:
        if connection:
            connection.close()
            print("Database connection as been closed!")         
            