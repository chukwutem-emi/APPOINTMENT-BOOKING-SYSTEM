from tables.dbModels import db
from flask_migrate import Migrate
from routes import blue_p
from flask import jsonify, Flask, request, render_template
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from extensions import mail
import logging
from flask_cors import CORS
from routes.utils.constants import FRONT_END_URL
load_dotenv()

def str_to_bool(value:str) -> bool:
    """
    convert common string representations of truthy/false value to boolean.
    Accept true/false, yes/no, 1/0, on/off (case insensitive)
    """
    if not value:
        return False
    return value.strip().lower() in ("true", "1", "yes", "on")

app = Flask(__name__)

MAINTENANCE_MODE = str_to_bool(os.getenv(key="MAINTENANCE_MODE", default="False"))

ATTACK_MODE = str_to_bool(os.getenv(key="ATTACK_MODE", default="False"))

ALLOW_IPS = os.getenv(key="ALLOW_IPS", default="127:0:0:1").split(",")

@app.before_request
def check_maintenance():
    if MAINTENANCE_MODE:
        client_ip = request.remote_addr
        if client_ip not in ALLOW_IPS:
            return render_template("maintenance.html"), 503
        
@app.before_request
def check_attack():
    if ATTACK_MODE:
        ip_address = request.remote_addr
        if ip_address not in ALLOW_IPS:
            return render_template("attack.html"), 503        

CORS(
    app,
    supports_credentials=True,
    origins=[FRONT_END_URL]
    # resources={r"/api/*":{"origins":"http://localhost:1234"}}
)
@app.route("/my-ip")
def my_ip():
    return {"flask_detected_ip":request.remote_addr}



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
