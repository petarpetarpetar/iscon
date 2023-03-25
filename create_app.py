from db import db
from app import app

def create_app():
    print("creating app")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
