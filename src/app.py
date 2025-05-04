from tables.dbModels import db
from flask_migrate import Migrate
from routes import blue_p
from flask import jsonify, Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from extensions import mail

load_dotenv()

app = Flask(__name__)

CORS(app=app)


base_uri=os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = base_uri

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = "chukwutememi@gmail.com"
app.config["MAIL_TLS"] = True
app.config["MAIL_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = "chukwutememi@gmail.com"

mail.init_app(app=app)

db.init_app(app=app)
mysql = MySQL()
mysql.init_app(app=app)


migrate = Migrate(app=app, db=db)

@app.route("/debug/routes", methods=["GET"])
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule})
    return jsonify(routes), 200

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message":"Welcome to Appointment booking system"}), 200

app.register_blueprint(blue_p, url_prefix="/api")
app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host= "0.0.0.0", port=port, debug=True)
