from tables.dbModels import db
from flask import jsonify, request, make_response
from routes.authentication.accessToken import token_required
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

@token_required
def create_personnel(current_user):
    if not current_user.admin:
        return jsonify({"personnelError":"You are not permitted to upload or create personnel. It is meant for admin users only"}), 401
    

    if request.method == "OPTIONS":
        return make_response("", 204)
    

    try:
        data = request.get_json("name")
        if not data or not data.get("name") or not data.get("role") or not data.get("specialization") or not data.get("organization")or not data.get("organization_address") or not data.get("email") or not data.get("phone_number"):
            return jsonify({"dataError":"Invalid request."}), 400
        

        required_fields = ["name", "role", "specialization", "organization", "organization_address" "email", "phone_number"]
        for field in required_fields:
            if field not in data:
                return jsonify({"missing":f"Missing required field.{field}"}), 400
            

        name                 = str(data["name"]).capitalize()
        role                 = str(data["role"])
        specialization       = str(data["specialization"])
        organization         = str(data["organization"])
        organization_address = str(data["organization_address"])
        email                = str(data["email"])
        phone_number          = str(data["phone_number"])


        with db.engine.connect() as connection:
            personnel_info = text("""
                INSERT INTO personnel(
                    name, role, specialization, organization, organization_address, email, phone_number
                ) VALUES(
                    :name, :role, :specialization, :organization, :email, :phone_number
                )
            """)
            connection.execute(statement=personnel_info, parameters={"name":name, "role":role, "specialization":specialization, "organization":organization, "organization_address":organization_address, "email":email, "phone_number":phone_number})
            connection.commit()

            return jsonify({"success":"Personnel created and uploaded successfully"}), 201
        
    except (KeyError, ValueError) as KV:
        return jsonify({"keyValueError":f"You input a wrong value in your payload"}), 400
    except SQLAlchemyError as e:
        return jsonify({"personnelDatabaseError":f"Network error or server not responding. This error originated from the server. {str(e)}"}), 500
    except Exception as E:
        return jsonify({"error":f"An error occurred at the course of uploading personnel into the database. {str(E)}"}), 500
