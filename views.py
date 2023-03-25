from flask import render_template
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity
from models.student import Student


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

def semesterList():
    return render_template("semesterList.html")

@jwt_required()
def studentProfil():
    id = get_jwt_identity()
    student = Student.find_by_id(id)
    return render_template("studentProfil.html", student=student)

def loginPage():
    return render_template("login.html")

def adminLoginPage():
    return render_template("adminLogin.html")

def dodavanjeSredstava():
    return render_template("dodavanjeSredstava.html")

def applyList():
    return render_template("applyList.html")

@jwt_required()
def transactionPage():
    id = get_jwt_identity()
    student = Student.find_by_id(id)
    return render_template("transaction.html", student=student)

def applyMenu():
    return render_template("applyMenu.html")