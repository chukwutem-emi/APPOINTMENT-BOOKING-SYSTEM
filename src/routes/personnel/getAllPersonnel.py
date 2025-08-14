from flask import request, jsonify, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tables.dbModels import db
from routes.authentication.accessToken import token_required

@token_required
def get_all_personnel(current_user):
    if not current_user.admin:
        return jsonify({"personnelErr": "Unauthorized!. Only admin users can perform this operation."}), 401
    

    if request.method == "OPTIONS":
        return make_response("", 204)
    

    try:
        with db.engine.connect() as connection:
            all_personnel = text("SELECT * FROM personnel")
            all_personnel_details = connection.execute(statement=all_personnel)
            all_personnel_data = all_personnel_details.fetchall()
            if len(all_personnel_data) == 0:
                return jsonify({"emptyDatabase": "The database is empty or does not contain personnel."}), 404
            

            personnel_list = []
            for personnel in all_personnel_data:
                if personnel not in personnel_list:
                    personnel_dict = {
                        "id":personnel.id,
                        "name":personnel.name,
                        "email":personnel.email,
                        "role":personnel.role,
                        "specialization":personnel.specialization,
                        "organization":personnel.organization,
                        "phone_number":personnel.phone_number,
                    }
                personnel_list.append(personnel_dict) 


            return jsonify({"all-personnel": personnel_list}), 200
        
    except Exception as e:
        return jsonify({"exception":f"An error has occurred. {str(e)}"}), 500
    except SQLAlchemyError as s:
        return jsonify({"serverErr":f"Internal server error. Server not responding"}), 500