from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from uuid import uuid4
db = SQLAlchemy()


@dataclass
class CarModel(db.Model):
    id:int
    car_uid:uuid4
    brand:str
    model: str
    registration_number:str
    power: int
    price: int
    type: str
    availability: bool

    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    car_uid = db.Column(db.String(36), nullable = False, default=lambda: str(uuid4()))
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    payment_uid = db.Column(db.String(36),nullable = False, default=lambda: str(uuid4()))
    car_uid = db.Column(db.String(36), nullable = False, default=lambda: str(uuid4()))
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    status=db.Column(db.Boolean, nullable=False)