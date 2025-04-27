from dotenv import load_dotenv
from flask import current_app
from flask_mail import Mail, Message
import os
from flask import jsonify

load_dotenv()


def send_mail(subject, receiver, body):
    try:
        with current_app.app_context():
            current_app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
            current_app.config["MAIL_PORT"] = 587
            current_app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
            current_app.config["MAIL_USERNAME"] = "chukwutememi@gmail.com"
            current_app.config["MAIL_TLS"] = True
            current_app.config["MAIL_SSL"] = False
            current_app.config["MAIL_DEFAULT_SENDER"] = "chukwutememi@gmail.com"

            mail = Mail(app=current_app)
            
        msg = Message(
            subject=subject,
            recipients=[receiver],
            body=body,
            sender="chukwutememi@gmail.com"
        )
        mail.send(message=msg)
    except Exception as e:
        return jsonify({"mail_error":f"An error occurred!. Mail not sent.{str(e)}"}), 500