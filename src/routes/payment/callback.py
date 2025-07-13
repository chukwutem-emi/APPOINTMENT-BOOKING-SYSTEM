from flask import request, jsonify, make_response


def payment_callback():
    if request.method == "OPTIONS":
        return make_response("", 204)
    try:
        status = request.args.get("status")

        if status == "success":
            return jsonify({"success_message":"Payment successful!"}), 200
        else:
            return jsonify({"failure_message":"Payment failed!"}), 200
    except Exception as e:
        return jsonify({"callback_error":f"An error has occurred:{str(e)}"}), 400