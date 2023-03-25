import bcrypt
from flask_restx import Resource, reqparse
from flask import jsonify, make_response, redirect, url_for
from sqlalchemy import false, true
from models.admin import Admin
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity

class AdminResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("ime", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("prezime", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")   
    
    def put(self): # registracija
        data = AdminResource.parser.parse_args()
        ime = data["ime"]
        prezime = data["prezime"]
        password = data["password"]

        student = Admin(password, ime, prezime) 
        student.save_to_db()

        return {"Message": f"New Admin created, id: {student.id}"}, 200
    
class AdminLoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=str, required=True, help="This field cannot be blank.") #TODO: CHANGE TO EMAIL
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = AdminLoginResource.parser.parse_args()
        userinfo = Admin.find_by_id(data['id'])

        if userinfo is None:
            return {"Message": "Error: User(ADMIN) does not exist"}, 401

        if bcrypt.checkpw(data["password"].encode("utf8"), userinfo.password):
            additional_claims = {"admin": True}

            access_token = create_access_token(identity=userinfo.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(userinfo.id, additional_claims=additional_claims)
            resp = make_response({"access_token_cookie": access_token, "refresh_token_cookie": refresh_token}, 200)
            resp.set_cookie("access_token_cookie", access_token, domain="192.168.137.80")
            resp.set_cookie("refresh_token_cookie", refresh_token, domain="192.168.137.80")
            resp.set_cookie("_user_id", str(userinfo.id).encode())

            return resp
        
        return {"Message": "Error: Password incorrect"}, 401
    
    @jwt_required(fresh=False)
    def delete(self): # logout
        resp = jsonify({"logout": True})

        resp.set_cookie("access_token_cookie", "", expires=0, domain="192.168.137.80")
        resp.set_cookie("refresh_token_cookie", "", expires=0, domain="192.168.137.80")

        return resp