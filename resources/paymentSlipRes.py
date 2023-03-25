from flask_restx import Resource, reqparse
from flask import jsonify, make_response, redirect, url_for
from sqlalchemy import false, true
from models.paymentSlip import PaymentSlip
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity
from models.student import Student

class PaymentSlipResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("student", type=str, required=False, help="This field cannot be blank.")
    parser.add_argument("svrhaUplate", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("vrstaPrihoda", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("opstina", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("bOrganizacija", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("pozivNaBroj", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("racunPrimaoca", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("kolicinaNovca", type=str, required=True, help="This field cannot be blank.")

    def get(self):
        return "healthy"
    
    @jwt_required()
    def post(self):
        data = PaymentSlipResource.parser.parse_args()
        svrhauplate = data["svrhaUplate"]
        vrstaPrihoda = data["vrstaPrihoda"]
        opstina = data["opstina"]
        bOrganizacija = data["bOrganizacija"]
        pozivNaBroj = data["pozivNaBroj"]
        racunPrimaoca = data["racunPrimaoca"] 
        kolicinaNovca = float(data["kolicinaNovca"][1:-3])
        
        student = Student.find_by_id(get_jwt_identity())
        if student.stanjeNaRacunu > kolicinaNovca:
            slip = PaymentSlip(get_jwt_identity(),svrhauplate, opstina, bOrganizacija, racunPrimaoca, pozivNaBroj, vrstaPrihoda, kolicinaNovca) 
            slip.save_to_db()
            student.stanjeNaRacunu -= kolicinaNovca
            student.save_to_db()
            return {"message": "Created"}, 200
        return {"message": "Error: Not enough funds!"}, 400
        

