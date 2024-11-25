from flaskFile import app
from tables.dbModels import db
from flask_migrate import Migrate
from routes import bp
from flask import jsonify
from flask_cors import CORS
import os



CORS(app=app)

migrate = Migrate(app=app, db=db)

@app.route("/debug/routes", methods=["GET"])
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({"endpoint": rule.endpoint, "methods": list(rule.methods), "url": rule.rule})
    return jsonify(routes), 200


app.register_blueprint(bp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host= "0.0.0.0", port=port, debug=True)
