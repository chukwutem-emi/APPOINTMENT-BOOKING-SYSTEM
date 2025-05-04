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
            print("📨 Inside send_async_mail, sending...")
            mail.send(message=msg)
        except Exception as e:
            print(f"[MAIL ERROR] An error occurred. Mail not sent: {str(e)}")
        
def send_mail(subject, receiver, body):
    print("📧 send_mail function called")
    app = current_app._get_current_object()
    current_app.logger.info("got current app info")
    current_app.logger.info(f"MAIL_CONFIG:{app.config}")
    msg = Message(
        subject=subject,
        recipients=[receiver],
        body=body,
        sender="chukwutememi@gmail.com"
    )
    Thread(target=send_async_mail, args=(app, msg, mail)).start()