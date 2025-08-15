from tables.dbModels import db
from routes.authentication.accessToken import token_required
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask import request, make_response, jsonify

@token_required
def get_personnel(current_user):
    if not current_user.admin:
        return jsonify({"requestErr":"Unauthorized user. Access denied!."}), 401
    

    if request.method == "OPTIONS":
        return make_response("", 204)
    

    try:
        data = request.get_json()
        if not data or not data.get("email"):
            return jsonify({"error":"Invalid input."}), 400
        

        required_field = ["email"]
        for item in required_field:
            if item not in data:
                return jsonify({"inputError":f"Missing require field{item}"}), 400
            

        email = str(data["email"])
        with db.engine.connect() as connection:
            a_personnel = text("SELECT * FROM personnel WHERE email=:email")
            personnel_data = connection.execute(statement=a_personnel, parameters={"email":email}).fetchone()
            personnel_info = personnel_data
            if not personnel_info or len(personnel_info) ==0:
                return jsonify({"message":"This particular personnel you are looking for is not found or does not exist in the database."}), 404
            
            personnel_dict = {
                "name"                 : personnel_info.name,
                "email"                : personnel_info.email,
                "role"                 : personnel_info.role,
                "organization"         : personnel_info.organization,
                "organization_address" : personnel_info.organization_address,
                "specialization"       : personnel_info.specialization,
                "phone_number"         : personnel_info.phone_number
            }
            return jsonify({"one-personnel": personnel_dict}), 200
        
    except (KeyError, ValueError) as kv:
        return jsonify({"keyValErr":f"Missing data or you entered a wrong input. {str(kv)}"}), 400
    except Exception as e:
        return jsonify({"exception":f"An error has occurred.{str(e)}"}), 500
    except SQLAlchemyError as s:
        return jsonify({"severErr":f"Server not responding. {str(s)}"}), 500