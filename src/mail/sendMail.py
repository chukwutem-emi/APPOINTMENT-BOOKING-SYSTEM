from dotenv import load_dotenv
from flask import current_app
from flask_mail import Message
import os
from flask import jsonify
from extensions import mail
from threading import Thread

load_dotenv()

def send_async_mail(app, msg, mail):
    with app.app_context():
        try:
            mail.send(message=msg)
        except Exception as e:
            print(f"[MAIL ERROR] An error occurred. Mail not sent: {str(e)}")
        
def send_mail(subject, receiver, body):
    app = current_app._get_current_object()
    sender=current_app.config["MAIL_DEFAULT_SENDER"]
    print(f"MAIL_DEFAULT_SENDER type: {type(sender)}, value: {sender}")
    msg = Message(
        subject=subject,
        recipients=[receiver],
        body=body,
        sender=sender
    )
    Thread(target=send_async_mail, args=(app, msg, mail)).start()