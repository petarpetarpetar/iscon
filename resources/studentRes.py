import bcrypt
from flask_restx import Resource, reqparse
from flask import jsonify, make_response, redirect, url_for
from sqlalchemy import false, true
from models.student import Student
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity

class StudentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("ime", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("prezime", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("jmbg", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("indeks", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("telefon", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("adresa", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")   
    parser.add_argument("studijskiProgram", type=str, required=True, help="This field cannot be blank.") 
    parser.add_argument("smer", type=str, required=True, help="This field cannot be blank.") 
    

    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        return id
    
    def put(self): # registracija
        data = StudentResource.parser.parse_args()
        ime = data["ime"]
        prezime = data["prezime"]
        jmbg = data["jmbg"]
        indeks = data["indeks"]
        telefon = data["telefon"]
        adresa = data["adresa"]
        email = data["email"]
        password = data['password']
        studijskiProgram = data['studijskiProgram']
        smer = data['smer']
        
        student = Student(password, ime, prezime, jmbg, indeks, studijskiProgram,telefon, email, adresa, smer) 
        student.save_to_db()

        return {"message": f"Created, id: {student.id}"}, 200
    
class StudentsListResource(Resource):
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if not claims['admin']:
            return {"message": "Not an admin"}, 401
        students =  [x.as_dict() for x in Student.find_all()]
        for s in students:
            s['password'] = ""

        print(students)
        return students
    

class StudentLoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=str, required=True, help="This field cannot be blank.") #TODO: CHANGE TO EMAIL
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = StudentLoginResource.parser.parse_args()
        userinfo = Student.find_by_id(data['id'])

        if userinfo is None:
            return {"message": "Error: User does not exist"}, 401

        if bcrypt.checkpw(data["password"].encode("utf8"), userinfo.password):
            additional_claims = {"admin": False}
            
            access_token = create_access_token(identity=userinfo.id,additional_claims=additional_claims)
            refresh_token = create_refresh_token(userinfo.id, additional_claims=additional_claims)
            resp = make_response({"access_token_cookie": access_token, "refresh_token_cookie": refresh_token}, 200)
            resp.set_cookie("access_token_cookie", access_token, domain="192.168.137.80")
            resp.set_cookie("refresh_token_cookie", refresh_token, domain="192.168.137.80")
            resp.set_cookie("_user_id", str(userinfo.id).encode())

            return resp
        
        return {"message": "Error: Password incorrect"}, 401
    
    @jwt_required(fresh=False)
    def delete(self): # logout
        resp = jsonify({"logout": True})

        resp.set_cookie("access_token_cookie", "", expires=0)
        resp.set_cookie("refresh_token_cookie", "", expires=0)

        return resp