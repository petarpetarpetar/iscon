from db import db

class Stundet(db.Model):
    __tablename__ = "students"

    # personal info
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    surname = db.Column(db.String(40))
    jmbg = db.Column(db.String(13)) # hardset for 13 digits as it is the maximum
    

    # studies info
    index = db.Column(db.String(15))
    phone = db.Column(db.String(20))

    country = db.Column(db.String(40))  # .
    city = db.Column(db.String(40))     # | combines all three to form adress
    street = db.Column(db.String(40))   # `

    
    