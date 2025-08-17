from flask import request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError as dbError
from tables.dbModels import AppointmentTypes, db
from routes.authentication.accessToken import token_required
from datetime import datetime, timedelta
from sqlalchemy import text as t
from mail.sendMail import send_mail
from routes.utils.appointmentGoogleCalender import book_appointment


@token_required
def career_counseling(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"Msg": "You are not permitted to perform this operation without login. Login required!"}), 401
    try:       
        data = request.get_json()
        if not data:
            return jsonify({"Data":"Invalid input!"}), 400
        
        required_fields = ["gender", "address", "next_of_kin", "next_of_kin_phone_number", "next_of_kin_address", "appointment_description", "appointment_time", "appointment_date", "name"]

        for field in required_fields:
            if field not in data:
                return jsonify({"careerCounseling_fieldError":f"Missing required field.:{field}"}), 400

        
        gender                   = str(data["gender"])
        address                  = str(data["address"])
        next_of_kin              = str(data["next_of_kin"])
        next_of_kin_phone_number = str(data["next_of_kin_phone_number"])
        next_of_kin_address      = str(data["next_of_kin_address"])
        name                     = str(data["name"]).capitalize()
        appointment_description  = str(data["appointment_description"])
        appointment_time_str     = str(data["appointment_time"])
        appointment_time         = datetime.strptime(appointment_time_str, "%H:%M").time()
        appointment_date_str     = str(data["appointment_date"])
        appointment_date         = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        duration                 = 90
        price                    = 40000

        end_time = (datetime.combine(date=appointment_date, time=appointment_time)+timedelta(minutes=duration)).time()
        
        
        with db.engine.connect() as connection:
            get_the_login_user = t("SELECT * FROM user WHERE public_id=:public_id")
            user_data = connection.execute(statement=get_the_login_user, parameters={"public_id":current_user.public_id}).fetchone()
            if len(user_data) ==0:
                return jsonify({"careerErrorMessage":"user not found!"}), 404
            user = user_data._asdict()
            user_id = user["id"]
            email_address = user["email_address"]
            phone_number  = user["phone_number"]
            username      = user["username"]
            

            get_personnel_data = t("SELECT * FROM personnel WHERE name=:name")
            personnel_info = connection.execute(statement=get_personnel_data, parameters={"name":name}).fetchone()
            if len(personnel_info) ==0:
                return jsonify({"careerPersonnel":"The career-counseling personnel you selected doesn't exist or he/she might have been deleted from the database."}), 404
            personnel_dict  = personnel_info._asdict()

            personnel_role       = personnel_dict["role"]
            organization_name    = personnel_dict["organization"]
            organization_address = personnel_dict["organization_address"]
            personnel_tel        = personnel_dict["phone_number"]
            personnel_id         = personnel_dict["id"]
            personnel_email      = personnel_dict["email"]


            summary     = f"This is an appointment for: \n{AppointmentTypes.CAREER_COUNSELING.value}"
            dateTime    = f"{appointment_date}T{appointment_time}+01:00"
            endDateTime = f"{appointment_date}T{end_time}+01:00"
            # capturing the response from book_appointment
            appointment_response, status_code = book_appointment(
                summary=summary,
                location=organization_address,
                description=appointment_description,
                dateTime=dateTime,
                email=email_address,
                endDateTime=endDateTime,
                personnel_email=personnel_email,
                user_id=user_id
            )
            if status_code == 401:
                return jsonify({
                    "error": "Google token invalid or expired. Re-authentication required.",
                    "re_auth_url": f"/api/bookApp/start-Oauth?user_id={user_id}"
                }), 401
            if status_code == 201:
                html_link = appointment_response.get("eventLink")
            else:
                return jsonify({"careerErr":"Failed to create calender event"}), 500
            
            
            user_appointment = t("""
                INSERT INTO appointment(
                    gender, user_phone_number, address, next_of_kin, next_of_kin_phone_number, next_of_kin_address, duration, price, appointment_types, user_id, appointment_time, appointment_date, appointment_description, appointment_endTime, personnel_id, personnel_role, organization_name, organization_address, personnel_tel, username 
                    ) VALUES(
                    :gender, :user_phone_number, :address, :next_of_kin,  :next_of_kin_phone_number, :next_of_kin_address, :duration, :price :appointment_types, :user_id, :appointment_time, :appointment_date, :appointment_description, :appointment_endTime, :personnel_id, :personnel_role, :organization_name , :organization_address, :personnel_tel, :username  
                    )
            """)

            connection.execute(statement=user_appointment, parameters={
                "gender":gender, "user_phone_number":phone_number, "address":address, "next_of_kin":next_of_kin, "next_of_kin_phone_number":next_of_kin_phone_number, "next_of_kin_address":next_of_kin_address, "duration":duration, "price":price,  "appointment_types":AppointmentTypes.CAREER_COUNSELING.value, "user_id":user_id, "appointment_time":appointment_time, "appointment_date":appointment_date, "appointment_description":appointment_description, "appointment_endTime":end_time, "personnel_id":personnel_id, "personnel_role":personnel_role, "organization_name": organization_name, "organization_address":organization_address, "personnel_tel":personnel_tel, "username":username
                })
            connection.commit()

            subject = f"ChEMSTEN => {organization_name}"
            body    = f"HI {username}!,\n\nCareer counseling appointment was booked successfully!,\nTime:{appointment_time},\nDate:{appointment_date},\nDuration:{duration}minutes,\nEndtime:{end_time},\nAddress:{organization_address},\nPersonnel-tel:{personnel_tel},\n\nThanks for using our service,\nBest regard,\nCHEMSTEN => {organization_name} Team."
            receiver = email_address
            send_mail(subject=subject, body=body, receiver=receiver)

            return jsonify({"Career_counseling":"☑️ Career counseling appointment was booked successfully!",
                            "googleCalenderEvent":html_link
                            }), 201
        
    except (KeyError, ValueError) as kvError:
        return jsonify({"careerCounseling_kvError":f"Invalid input!.:{str(kvError)}"}), 400
    except dbError as d:
        return jsonify({"careerCounseling_dbError":f"Database/server error: {str(d)}"}), 500
    except Exception as E:
        return jsonify({"careerCounseling_exc": f"An error occurred: {str(E)}"}), 500