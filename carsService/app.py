from email import message
import os 
import sys
from marshmallow import ValidationError
import psycopg2
from flask import Flask, request, flash, redirect
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, url_for
from flask_sqlalchemy import SQLAlchemy
from carsDB import CarDB
# from utils import make_data_response, make_empty
from flask import send_from_directory, jsonify, make_response
from sqlalchemy import exc
from model import CarModel, db
import uuid
import datetime

app = Flask(__name__)

db.init_app(app)

migrate = Migrate(app)

port = os.environ.get('PORT')
if port is None:
    port = 8070

@app.errorhandler(404)



def make_data_response(status_code, **kwargs):
    response = jsonify({
            **kwargs
        })
    response.status_code = status_code
    return response

def make_empty(status_code):
    response = make_response()
    response.status_code = status_code
    del response.headers["Content-Type"]
    del response.headers["Content-Length"]
    return response



@app.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route("api/v1/rental/<string:carUid>", methods = ["GET"])
def get_car(car_uid):
    """Получить информацию о всех арендах пользователя"""
    result=CarDB.session.query(CarModel).filter(CarModel.rental_uid==car_uid).one_or_none()
    if not result:
        abort(404)
    return make_response(jsonify(result), 200)

@app.route("api/v1/cars/<string:carUid>/order", methods = ["DELETE"])
def delete_one_rental(car_uid):
    car = CarDB.session.query(CarModel).filter(CarModel.rental_uid==car_uid).one_or_none()
    car.availability = True

    try:
        db.session.commit()
        return make_empty(204)
    except:
        db.session.rollback()
        return make_data_response(500, message="Database delete error")


@app.route("api/v1/cars/>", methods = ["GET", "POST"])
def get_all_rental():
    if request.method == 'GET':
        result=CarModel.query.all()
        if not result:
            abort(404)
        return make_response(jsonify(result), 200)

    if request.method == "POST":
        try:
            if request.is_json:
                user = request.headers['X-User-Name']
                data = request.get_json()
                new_rental = CarModel(
                    rental_uid = str(uuid.uuid4),
                    username = user,
                    car_uid = uuid.UUID(data["car_uid"]),
                    date_from = datetime.datetime.strptime(data['dateFrom'], "%Y-%m-%d").date(),
                    date_to = datetime.datetime.strptime(data['dateTo'], "%Y-%m-%d").date(),
                    status = "IN_PROGRESS",
                )
            
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
    
        try:
            db.session.add(new_rental)
            db.session.commit()
            # return make_data_response(200, message="Successfully added new person: name: {}, address: {}, work: {}, age: {} ".format(new_person.name, 
            # new_person.address, new_person.work, new_person.age))
        except:
            db.session.rollback()
            return make_data_response(500, message="Database add error!")

    response = make_empty(201)
    response.headers["Location"] = f"/api/v1/persons/{new_rental.id}"
    return response




