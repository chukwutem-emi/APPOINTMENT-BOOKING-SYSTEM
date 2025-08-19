from flask import request, jsonify, make_response
from routes.authentication.accessToken import token_required
from tables.dbModels import db, AppointmentTypes
from datetime import datetime, timedelta
from sqlalchemy import text as t
from sqlalchemy.exc import SQLAlchemyError as dbError
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment

@token_required
def home_service(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"home_service_error": "Unauthorized to carry out home service appointment operation. Login required!"}), 401
    try:       
        data = request.get_json()
        if not data:
            return jsonify({"home_service_data_error":"Invalid input!"}), 400
        
        required_fields = ["gender", "address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "appointment_time", "appointment_date", "appointment_description", "name"]

        for field in required_fields:
            if field not in data:
                return jsonify({"home_service_input_error":f"Missing required field:{field}"}), 400

        gender                   = str(data["gender"])
        address                  = str(data["address"])
        name                     = str(data["name"]).capitalize()
        next_of_kin              = str(data["next_of_kin"])
        next_of_kin_phone_number = str(data["next_of_kin_phone_number"])
        next_of_kin_address      = str(data["next_of_kin_address"])
        appointment_description  = str(data["appointment_description"])
        appointment_time_str     = str(data["appointment_time"])
        appointment_time         = datetime.strptime(appointment_time_str, "%H:%M").time()
        appointment_date_str     = str(data["appointment_date"])
        appointment_date         = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        phone_repair_price       = "It depends on the type of the faults/damages"
        laptop_repair_price      = "It depends on the type of the faults/damages"
        price                    = 80000
        duration                 = 240

        end_time = (datetime.combine(date=appointment_date, time=appointment_time) + timedelta(minutes=duration)).time()
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if len(user_data) == 0:
                return jsonify({"homeServiceErrorMessage":"user not found!"}), 404
            user = user_data._asdict()

            user_id       = user["id"]
            email_address = user["email_address"]
            phone_number  = user["phone_number"]
            username      = user["username"]

            get_personnel_info = t("SELECT * FROM personnel WHERE name=:name")
            personnel_data = connection.execute(statement=get_personnel_info, parameters={"name":name}).fetchone()
            if len(personnel_data) == 0:
                return jsonify({"message":"The home-service personnel you selected doesn't exist, or he/she might have been deleted from the database."}), 404
            personnel_dict = personnel_data._asdict()

            personnel_role       = personnel_dict["role"]
            organization_name    = personnel_dict["organization"]
            organization_address = personnel_dict["organization_address"]
            personnel_tel        = personnel_dict["phone_number"]
            personnel_id         = personnel_dict["id"]
            personnel_email      = personnel_dict["email"]

            
            summary     = f"This is an appointment for:\n{AppointmentTypes.ELECTRONICS_REPAIR.value}"
            dateTime    = f"{appointment_date}T{appointment_time}+01:00"
            endDateTime = f"{appointment_date}T{end_time}+01:00"
            # capturing the response from book_appointment:
            appointment_response, status_code = book_appointment(
                summary=summary, 
                location=organization_address, 
                description=appointment_description, 
                dateTime=dateTime, 
                email=email_address,
                endDateTime=endDateTime,
                user_id=user_id,
                personnel_email=personnel_email
                )
            if status_code == 401:
                return jsonify({
                    "error": "Google token invalid or expired. Re-authentication required.",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({"HomeServiceErr": "Failed to create google calender event",
                        "Details":appointment_response
                        }), 500

            user_appointment = t("""
                INSERT INTO appointment(
                    gender, user_phone_number, address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, phone_repair_price, price, laptop_repair_price, appointment_types, user_id, appointment_time, appointment_date, appointment_description, duration, appointment_endTime, username, personnel_role, organization_name, personnel_tel, personnel_id, organization_address
                    ) VALUES(
                    :gender, :user_phone_number, :address, :next_of_kin,  :next_of_kin_phone_number, :next_of_kin_address, :phone_repair_price, :price, :laptop_repair_price, :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :duration, :appointment_endTime, :username, :personnel_role, :organization_name, :personnel_tel, :personnel_id, :organization_address
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "gender":gender, "user_phone_number":phone_number, "address":address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "phone_repair_price":phone_repair_price, "price":price, "laptop_repair_price":laptop_repair_price, "appointment_types":AppointmentTypes.HOME_SERVICES.value, "user_id":user_id, "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "duration":duration, "appointment_endTime":end_time, "username":username, "personnel_role":personnel_role, "organization_name":organization_name, "personnel_tel":personnel_tel, "personnel_id":personnel_id, "organization_address":organization_address
                })
            connection.commit()

            subject = f"CHEMSTEN => {organization_name}"
            body    = f"HI {username}!,\n\nHome service appointment was booked successfully!,\nTime:{appointment_time},\nDate:{appointment_date},\nDuration:{duration},\nEndtime:{end_time},\nAddress:{organization_address},\nPersonnel-tel:{personnel_tel},\n\nThanks for using our service,\nBest regard,\nCHEMSTEN => {organization_name} Team."
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)


            return jsonify({"home_service":"☑️ Home service appointment was booked successfully!",
                            "googleCalendarEvent":html_link
                            }), 201

    except (KeyError, ValueError) as KvError:
        return jsonify({"home_service_kvError":f"Invalid input!:{str(KvError)}"}), 400
    except Exception as e:
        return jsonify({"home_service_Exc":f"An error occurred during your home service booking appointment operation: {str(e)}"}), 500
    except dbError as d:
        return jsonify({"home_service_DB_error":f"Database/server error: {str(d)}"}), 500