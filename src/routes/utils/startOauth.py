from flask import request, jsonify, current_app
from routes.utils.start0authFun import oauth_function


def start_oauth():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user_id in query parameters. Please provide a valid user_id"}), 400

        return oauth_function(user_id=user_id)

    except ValueError as ve:
        current_app.logger.error(f"Configuration error: {ve}")
        return jsonify({"error": str(ve)}), 500

    except Exception as e:
        current_app.logger.exception("Unexpected error during OAuth start")
        return jsonify({
            "error": "An unexpected error occurred during the OAuth process",
            "details": str(e)
        }), 500
