from flask_restx import Resource, reqparse
from flask import jsonify, make_response, redirect, url_for
from sqlalchemy import false, true
from models.paymentSlip import PaymentSlip
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity

class PaymentSlipResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("student", type=str, required=False, help="This field cannot be blank.")
    parser.add_argument("svrhauplate", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("vrstaPrihoda", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("opstina", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("bOrganizacija", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("pozivNaBroj", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("racunPrimaoca", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("kolicinaNovca", type=str, required=True, help="This field cannot be blank.")

    def get(self):
        return "healthy"
    
    def post(self):
        data = PaymentSlipResource.parser.parse_args()
        student = None # id studenta ja cu generisati u parseru
        svrhauplate = data["svrhauplate"]
        vrstaPrihoda = data["vrstaPrihoda"]
        opstina = data["opstina"]
        bOrganizacija = data["bOrganizacija"]
        pozivNaBroj = data["pozivNaBroj"]
        
        slip = PaymentSlip(student, svrhauplate, vrstaPrihoda, opstina, bOrganizacija, pozivNaBroj) 
        slip.save_to_db()

        return {"Message": "Created"}, 200
    

