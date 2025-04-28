from tables.dbModels import db
from flask_migrate import Migrate
from routes import blue_p
from flask import jsonify, Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

CORS(app=app)


base_uri=os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = base_uri

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host= "0.0.0.0", port=port, debug=True)
