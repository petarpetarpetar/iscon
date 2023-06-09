from db import db

class PaymentSlip(db.Model):
    __tablename__ = "paymentslips"

    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey("students.id"))
    # ime prezime broj telefona adresa

    svrhauplate = db.Column(db.String(100))
    opstina = db.Column(db.String(100))
    bOrganizacija = db.Column(db.String(100))
    racunPrimaoca = db.Column(db.String(50))
    pozivNaBroj = db.Column(db.String(100))
    vrstaPrihoda = db.Column(db.String(30))
    kolicinaNovca = db.Column(db.Float)


    def __init__(self, student, svrhauplate, opstina, bOrganizacija, racunPrimaoca, pozivNaBroj, vrsaPrihoda, kolicinaNovca): 
        self.svrhauplate = svrhauplate 
        self.opstina = opstina 
        self.bOrganizacija = bOrganizacija 
        self.pozivNaBroj = pozivNaBroj
        self.racunPrimaoca = racunPrimaoca
        self.vrstaPrihoda = vrsaPrihoda
        self.kolicinaNovca = kolicinaNovca
        self.student = student
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by(cls, key, value):
        return cls.query.filter_by(key=value).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()