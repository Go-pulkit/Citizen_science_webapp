from flask_sqlalchemy import SQLAlchemy
from app import *
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Create instances of the db.Model class to create the database tables
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    email = db.Column(db.String(50), index = True, unique = True)
    #password = db.Column(db.password, unique = False)
    age = db.Column(db.Integer, unique = False)
    state = db.Column(db.String(30), unique = False)
    user = db.relationship('Sight', backref = 'Users', lazy = 'dynamic')
    
    def __repr__(self):
        return '<Users {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(generate_password_hash(password), password)    

class Sight(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    place = db.Column(db.String(30), index = True, unique = False)
    count = db.Column(db.Integer, index = True, unique = False)
    time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    common_name = db.Column(db.String(50), unique = True, index = True)


#activate the database
db.create_all()    

