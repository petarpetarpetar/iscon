from db import db
import bcrypt

class Student(db.Model):
    __tablename__ = "students"

    # personal info
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(40))
    prezime = db.Column(db.String(40))
    jmbg = db.Column(db.String(13)) # hardset for 13 digits as it is the maximum

    # studies info
    indeks = db.Column(db.String(15))
    telefon = db.Column(db.String(20))
    email = db.Column(db.String(40))
    adresa = db.Column(db.String(150)) 
    smer = db.Column(db.String(30))
    godina = db.Column(db.String(10))
    studijskiProgram = db.Column(db.String(30))
    semestar = db.Column(db.Integer)
    ukupnoUplaceno = db.Column(db.Float)

    stanjeNaRacunu = db.Column(db.Float)
    # security
    password = db.Column(db.String(128)) #

    
    def __init__(self, password, ime, prezime, jmbg, indeks, studijskiProgram, telefon, email, adresa, smer):
        self.ime = ime
        self.prezime = prezime
        self.jmbg = jmbg
        self.indeks = indeks
        self.telefon = telefon
        self.email = email
        self.smer = smer
        self.studijskiProgram = studijskiProgram
        self.ukupnoUplaceno = 0.0
        self.adresa = adresa
        self.stanjeNaRacunu = 0.0
        self.godina = "1. godina"
        self.semestar = 1
        # Hashing the password with random salt
        hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        self.password =  hashed_password
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def topup(cls, _id, amount):
        student = cls.find_by_id(_id)
        if student.stanjeNaRacunu == None:
            student.stanjeNaRacunu = 0
        student.stanjeNaRacunu += amount
        student.ukupnoUplaceno += amount
        student.save_to_db()
        return True