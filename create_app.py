from db import db
from app import app

def create_app():
    db.init_app(app)
    return app
