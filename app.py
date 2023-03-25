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
from resources.paymentSlipRes import PaymentSlipResource
from resources.studentRes import StudentResource, StudentsListResource, StudentLoginResource
from resources.adminRes import AdminLoginResource, AdminResource
from resources.paypalRes import PaypalCreatePayment, PaypalExecutePayment
app = Flask(__name__)


# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "7hol100vGE8y1gk2y3b4ASDkj768VinAc7y1823b4jDA"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_CSRF_CHECK_FORM"] = False
app.config["JWT_COOKIE_SECURE"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app, doc=False)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#api.add_resource(UserRegister, "/register")

#app.add_url_rule("/home/google756ae359b1032929.html", view_func=views.google_verify)
app.add_url_rule("/home", view_func=views.home)
app.add_url_rule("/courseList", view_func=views.courseList)
app.add_url_rule("/semesterList", view_func=views.semesterList)
app.add_url_rule("/studentProfil", view_func=views.studentProfil)
app.add_url_rule("/loginPage", view_func=views.loginPage)
app.add_url_rule("/adminLogin", view_func=views.adminLoginPage)
app.add_url_rule("/dodavanjeSredstava", view_func=views.dodavanjeSredstava)
app.add_url_rule("/applyList", view_func=views.applyList)
app.add_url_rule("/transaction", view_func=views.transactionPage)
app.add_url_rule("/applyMenu", view_func=views.applyMenu)
app.add_url_rule("/adminProfile", view_func=views.adminProfile)
app.add_url_rule("/imageUpload", methods=['POST'], view_func=views.upload)
app.add_url_rule("/nextSemester", methods=['POST'], view_func=views.semestar)
app.add_url_rule("/registerStudent", view_func=views.registerStudent)
app.add_url_rule("/studentList", view_func=views.studentList)

api.add_resource(PaymentSlipResource, "/paymentSlip")

api.add_resource(PaypalCreatePayment, "/payment/paypal/create/<amount>")
api.add_resource(PaypalExecutePayment, "/payment/paypal/execute")

api.add_resource(StudentResource, "/student")
api.add_resource(StudentsListResource, "/studentsList")
api.add_resource(StudentLoginResource, "/login")


api.add_resource(AdminLoginResource, "/adminLogin")
api.add_resource(AdminResource, "/admin")

HOME = "http://localhost:5000"

@jwt.unauthorized_loader
def failed_loader(_err):
    return render_template("login.html")

@jwt.expired_token_loader
def expired(header, payload):
    return render_template("login.html")


@app.after_request
def refresh_expiring_jwts(response):
    print(f"{request.endpoint=}")
    if request.endpoint == "student_login_resource":
        print("returning as normal")
        return response
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        additional_claims = {"admin":get_jwt()['admin']}
        if target_timestamp > exp_timestamp:
            
            access_token = create_access_token(identity=get_jwt_identity(), additional_claims=additional_claims)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def start():
    from create_app import create_app

    app = create_app()
    with app.app_context():
        db.create_all()
    port = 5000
    app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()


