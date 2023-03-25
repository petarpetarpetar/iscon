from db import db
import bcrypt

class Admin(db.Model):
    __tablename__ = "admins"

    # personal info
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(40))
    prezime = db.Column(db.String(40))

    # security
    password = db.Column(db.String(128)) #

    def __init__(self, password, ime, prezime):
        self.ime = ime
        self.prezime = prezime
        # Hashing the password with random salt
        hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        self.password =  hashed_password

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