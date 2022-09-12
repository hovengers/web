from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
