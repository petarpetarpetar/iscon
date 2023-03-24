from db import db

class PaymentSlip(db.Model):
    __tablename__ = "paymentslips"

    id = db.Column(db.Integer, primary_key=True)
    student = id.Column(db.Integer, db.ForeignKey("students.id"))
    # ime prezime broj telefona adresa

    # primalac<string>
    # svrhauplate<string>
    # vrstaprihoda<string>
    # opstina
    # budzetska organizacija
    # poziv na broj
    # iznos
