from tables.dbModels import db
from flask_migrate import Migrate
from routes import blue_p
from flask import jsonify, Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from extensions import mail
import logging

load_dotenv()

app = Flask(__name__)

CORS(
    app=app,
    origins=["http://locahost:1234"],
    supports_credentials=True,
    methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# set logging level to INFO
app.logger.setLevel(logging.INFO)

# Customize the format
formatter = logging.Formatter(
    "[%(asctime)s] %(levelName)s in %(module)s: %(message)s"
    )

# setting up handlers
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

#  Avoiding duplicate logs in the console
if not app.logger.handlers:
    app.logger.addHandler(console_handler)

app.logger.info("☑️ Flask logger configured and running")



base_uri = os.getenv("SQLALCHEMY_DATABASE_URI").replace(r"\x3a", ":")
app.config["SQLALCHEMY_DATABASE_URI"] = base_uri


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"    
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_SSL"] = os.getenv("MAIL_SSL", "False") == "False"
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail.init_app(app=app)

db.init_app(app=app)
mysql = MySQL()
mysql.init_app(app=app)


migrate = Migrate(app=app, db=db)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message":"Welcome to Appointment booking system"}), 200


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


app.register_blueprint(blue_p, url_prefix="/api")

@app.route("/debug/routes", methods=["GET"])
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule})
    return jsonify(routes), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host= "0.0.0.0", port=port, debug=True)
