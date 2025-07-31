from routes.authentication.accessToken import token_required
from flask import jsonify, current_app, make_response, request
from tables.dbModels import db
from sqlalchemy import text as t

@token_required
def clear_google_token(current_user):
    if request.method == "OPTIONS":
        return make_response("", 204)
    if not current_user:
        return jsonify({"Google token err": "You are not allowed to perform this operation. Login required"}), 403
    try:
        with db.engine.connect() as connection:
            clear_token = t("UPDATE `user` SET google_token = NULL WHERE public_id=:public_id")
            affected_column = connection.execute(statement=clear_token, parameters={"public_id":current_user.public_id})
            result = affected_column
            connection.commit()
            if result.rowcount == 0:
                return jsonify({"token-column-err": "User not found in the database"}), 404
            current_app.logger.info(f"Cleared google token for user: {current_user}")
            return jsonify({"Cleared":"Token cleared"}), 200
    except Exception as e:
        current_app.logger.exception("Failed to clear google token from database")
        return jsonify({"Clearing-token-err":str(e)}), 500
    