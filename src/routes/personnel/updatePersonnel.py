from tables.dbModels import db
from flask import jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from routes.authentication.accessToken import token_required

@token_required
def update_personnel(current_user):
    if not current_user.admin:
        return jsonify({"access":"Unauthorized!. Access denied."}), 401
    

    if request.method == "OPTIONS":
        return make_response("", 204)
    

    try:
        data = request.get_json()
        if not data or not data.get("name") or not data.get("role") or not data.get("email") or not data.get("specialization") or not data.get("phone_number") or not data.get("organization"):
            return jsonify({"invalid": "Invalid request!."}), 400
        

        required_fields = ["name", "role", "email", "specialization", "phone_number", "organization"]
        for field in required_fields:
            if field not in data:
                return jsonify({"missing":f"Missing required field. {field}"}), 400
            

        specialization       = str(data["specialization"]).capitalize()
        organization_address = str(data["organization_address"]).capitalize()
        organization         = str(data["organization"]).capitalize()
        phone_number         = str(data["phone_number"])
        email                = str(data["email"])
        name                 = str(data["name"]).capitalize()
        role                 = str(data["role"]).capitalize()
        with db.engine.connect() as connection:
            update_personnel_info = text("""
                    UPDATE personnel SET specialization=:specialization, organization=:organization, organization_address=:organization_address, phone_number=:phone_number, email=:email, name=:name, role=:role WHERE email=:email
            """)
            update_personnel_data = connection.execute(statement=update_personnel_info, parameters={"specialization":specialization, "organization":organization, "organization_address":organization_address, "phone_number":phone_number, "email":email, "name":name, "role":role})
            if update_personnel_data.rowcount == 0 :
                return jsonify({"message":"Personnel does not exist or  He/She could have been deleted from the database"}), 404
            connection.commit()


            return jsonify({"updated":"Personnel information was updated successfully!."}), 200
        
    except (KeyError, ValueError) as kv:
        return jsonify({"keyValueError":f"An error due to key/value has occurred. Check your input. {str(kv)}"}), 400
    except Exception as e:
        return jsonify({"exception":f"An error as occurred. {str(e)}"}), 500
    except SQLAlchemyError as s:
        return jsonify({"serverError":f"The server not responding or it might have encountered some errors. {str(s)}"}), 500