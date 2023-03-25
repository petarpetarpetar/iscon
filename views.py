import os

from flask import render_template, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity
from models.student import Student
from models.paymentSlip import PaymentSlip


def home():
    return "<p>Hello</p>"

@jwt_required()
def courseList():
    student = Student.find_by_id(_id=get_jwt_identity())
    temp = {
        "Програмски језици I": 	                        [3, 7, "3+1+2", "O"],
        "Структуре података и алгоритми": 	            [3,	7, "3+1+2", "O"],
        "Основи електронике и дигиталне технике": 	    [3, 6, "3+1+1", "O"],
        "Дискретна математика": 	                    [3, 5, "2+2+0","O"],
        "Основи софтверског инжењерства": 	            [3, 5, "3+0+1", "O"],
        "Математика IV": 	                            [4, 6, "3+2+0", "O"],
        "Програмски језици II":                         [4, 7, "3+1+2", "O"],
        "Основи оперативних система":                   [4, 5, "3+0+1", "O"],
        "Основи комуникација и теорија информација":    [4, 5, "2+1+1", "O"],
        "Формалне методе у софтверском инжењерству":    [4, 7, "3+1+2", "O"]
    }


    return render_template("courseList.html", temp=temp, student=student)

@jwt_required()
def semesterList():
    student = Student.find_by_id(_id=get_jwt_identity())
    temp = {
        "Програмски језици I": 	                        [3, 7, "3+1+2", "O"],
        "Структуре података и алгоритми": 	            [3,	7, "3+1+2", "O"],
        "Основи електронике и дигиталне технике": 	    [3, 6, "3+1+1", "O"],
        "Дискретна математика": 	                    [3, 5, "2+2+0","O"],
        "Основи софтверског инжењерства": 	            [3, 5, "3+0+1", "O"],
        "Математика IV": 	                            [4, 6, "3+2+0", "O"],
        "Програмски језици II":                         [4, 7, "3+1+2", "O"],
        "Основи оперативних система":                   [4, 5, "3+0+1", "O"],
        "Основи комуникација и теорија информација":    [4, 5, "2+1+1", "O"],
        "Формалне методе у софтверском инжењерству":    [4, 7, "3+1+2", "O"]
    }

    return render_template("semesterList.html", student=student, temp=temp)

@jwt_required()
def studentProfil():
    id = get_jwt_identity()
    student = Student.find_by_id(id)
    return render_template("studentProfil.html", student=student)

def loginPage():
    return render_template("login.html")

def adminLoginPage():
    return render_template("adminLogin.html")

@jwt_required()
def adminProfile():
    return render_template("adminProfile.html")

@jwt_required()
def dodavanjeSredstava():

    all = PaymentSlip.find_all()
    return render_template("dodavanjeSredstava.html", paymentSlips = all)

@jwt_required()
def applyList():
    id = get_jwt_identity()
    student = Student.find_by_id(id)
    return render_template("applyList.html", student=student)

@jwt_required()
def transactionPage():
    id = get_jwt_identity()
    student = Student.find_by_id(id)
    return render_template("transaction.html", student=student)

@jwt_required()
def applyMenu():
    return render_template("applyMenu.html")

@jwt_required()
def semestar():
    identity = get_jwt_identity()
    
    student = Student.find_by_id(identity)
    if student.stanjeNaRacunu > 42:
        student.stanjeNaRacunu -= 42
        student.semestar += 1
        student.save_to_db()
        return {"message":"ok"},200
    return {"message":"Error: nedovoljno sredstava"},400
    

def upload():
    if request.method == 'POST':
        print(request.files)
        file = request.files['file']
        print(file)
        file.save(os.path.join('/home/petarm/Documents/banjaluka/static/images/uploads', file.filename))
        return 'Image uploaded successfully!'
    return {"message": 'Image uploaded successfully!'}, 200

def registerStudent():
    return render_template("registerStudent.html")

@jwt_required()
def studentList():
    return render_template("studentList.html")