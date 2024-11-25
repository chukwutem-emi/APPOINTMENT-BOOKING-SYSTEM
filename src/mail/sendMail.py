from dotenv import load_dotenv
from flaskFile import app
from flask_mail import Mail, Message
import os
from flask import jsonify

load_dotenv()

app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = "chukwutememi@gmail.com"
app.config["MAIL_TLS"] = True
app.config["MAIL_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = "chukwutememi@gmail.com"


mail = Mail(app=app)

def send_mail(subject, receiver, body):
    try:
        msg = Message(
            subject=subject,
            recipients=[receiver],
            body=body,
            sender="chukwutememi@gmail.com"
        )
        mail.send(message=msg)
    except Exception as e:
        return jsonify({"mail_error":f"An error occurred!. Mail not sent.{str(e)}"}), 500