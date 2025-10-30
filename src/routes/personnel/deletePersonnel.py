from tables.dbModels import db
from sqlalchemy.exc import SQLAlchemyError
from flask import request, jsonify, make_response
from sqlalchemy import text
from routes.authentication.accessToken import token_required

@token_required
def delete_personnel(current_user):
    if not current_user.admin:
        return jsonify({"deleteError": "You are non-admin user. Unauthorized!."}), 401
    

    if request.method == "OPTIONS":
        return make_response("", 204)
    

    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"inputError": "Invalid input!"}), 400
    

    required_field = ["name"]
    for item in required_field:
        if item not in data:
            return jsonify({"missing":f"Missing required field. {item}"}), 400
        
    try:   
        name = str(data["name"]).strip()
        with db.engine.connect() as connection:
            delete = text("DELETE FROM personnel WHERE name=:name")
            personnel_info = connection.execute(statement=delete, parameters={"name":name})
            personnel_data = personnel_info


            if personnel_data.rowcount == 0:
                return jsonify({"notFound": "We could'nt found the personnel from the database. It could be either the personnel does not exist or He/She has been deleted already before now."}), 404
            connection.commit()


            return jsonify({"deleted":"The deletion of personnel was successful"}), 200
        
    except (KeyError, ValueError) as kv:
        return jsonify({"keyValErr":f"Key/value error has occurred. Please check your input.{str(kv)}"}), 400
    except Exception as e:
        return jsonify({"exception":f"An error has occurred. {str(e)}"}), 500
    except SQLAlchemyError as s:
        return jsonify({"databaseErr":f"Server/database error. {str(s)}"}), 500