from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid


from werkzeug.security import generate_password_hash, check_password_hash


import secrets


from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref='owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)



class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    year = db.Column(db.String(4))
    make = db.Column(db.String(30))
    model = db.Column(db.String(30))
    miles = db.Column(db.String(7))
    color = db.Column(db.String(30))
    horsepower = db.Column(db.String(5))
    torque = db.Column(db.String(5))
    modifications = db.Column(db.String(300))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, year, make, model, miles, color,
                horsepower, torque, modifications, user_token, id = ''):
        
        self.id = self.set_id()
        self.year = year
        self.make = make
        self.model = model
        self.miles = miles
        self.color = color
        self.horsepower = horsepower
        self.torque = torque
        self.modifications = modifications
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())


class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'year','make', 'model', 'miles', 'color', 'horsepower', 'torque', 'modifications']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)