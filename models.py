from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """A table that represents a User"""

    __tablename__ = "users"

    username = db.Column(db.String(20),primary_key=True,unique=True)

    password = db.Column(db.String,nullable=False)

    email = db.Column(db.String(50),nullable=False,unique=True)

    first_name = db.Column(db.String(30),nullable=False)

    last_name = db.Column(db.String(30),nullable=False)
    
    def register(self):
        hashed = Bcrypt().generate_password_hash(self.password)
        hashed_utf8 = hashed.decode("utf8")
        self.password=hashed_utf8

        db.session.add(self)
        db.session.commit()
        return self

    def authenticate(self,pwd_attempt):
        return Bcrypt().check_password_hash(self.password,pwd_attempt)

class Feedback(db.Model):
    """A table that represants feedback"""
    
    __tablename__ = "feedback"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.String(100),nullable=False)

    content = db.Column(db.String(1000),nullable=False)

    username = db.Column(db.String(20),db.ForeignKey('users.username'))

    user = db.relationship("User",backref="feedback")