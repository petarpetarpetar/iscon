import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for, make_response
from flask_restx import Api
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    create_access_token,
    jwt_required,
    JWTManager,
    set_access_cookies,
    unset_jwt_cookies
)
from flask_cors import CORS

import views
from db import db
from models.student import Stundet
from models.paymentSlip import PaymentSlip

app = Flask(__name__)

# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

api = Api(app, doc=False)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#api.add_resource(UserRegister, "/register")

#app.add_url_rule("/home/google756ae359b1032929.html", view_func=views.google_verify)
app.add_url_rule("/home", view_func=views.home)


HOME = "http://localhost:5000"

@jwt.unauthorized_loader
def failed_loader(_err):
    print(_err)
    try:
        if get_jwt():
            users_online, new_orders, total_orders = views.get_stats_numbers()

            resp = make_response(render_template("new_home.html",users_online=users_online, new_orders=new_orders, total_orders=total_orders, alert="relogin", timestamp=time.time(), port=os.environ.get("PORT", 5000)))
            return resp
    except:
        return redirect(HOME)


@jwt.expired_token_loader
def expired(header, payload):
    users_online, new_orders, total_orders = views.get_stats_numbers()
    return render_template("new_home.html", users_online=users_online, new_orders=new_orders, total_orders=total_orders,alert="relogin", timestamp=time.time(), port=os.environ.get("PORT", 5000))


@app.after_request
def refresh_expiring_jwts(response):
    if request.endpoint == "user_logout":
        return response
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def start():
    from create_app import create_app

    app = create_app()

    port = 5000

    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
