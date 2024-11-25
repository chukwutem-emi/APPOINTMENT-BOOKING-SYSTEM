from functools import wraps
from tables.dbModels import User
from flask import request, jsonify as J
import jwt
from flaskFile import  app
import os
from dotenv import load_dotenv

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if "access-token" in request.headers:
            token=request.headers["access-token"]
            if token and token.startswith("Bearer "):
                token=token.split(" ")[1]
            else:
                return J({"Prefix":"Invalid token prefix!"}), 400
        if not token:
            return J({"Missing":"Token is missing!, please login to get an access token"}), 401
        try:
            data = jwt.decode(jwt=token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=User.query.filter_by(public_id=data["public_id"]).first()
        except jwt.ExpiredSignatureError:
            return J({"Expired": "Your token has expired!, the estimated time for the token to expire is after 60-minutes of your login. please you can login again or try again later."}), 401
        except jwt.InvalidTokenError:
            return J({"InvalidToken": "You provided an Invalid token!"}), 401
        return f(current_user=current_user, *args, **kwargs)
    return decorated