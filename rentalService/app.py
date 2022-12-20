from email import message
import os 
import sys
from marshmallow import ValidationError
import psycopg2
from flask import Flask, request, flash, redirect
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, url_for
from flask_sqlalchemy import SQLAlchemy
from rentalDB import RentalDB
# from utils import make_data_response, make_empty
from flask import send_from_directory, jsonify, make_response
from sqlalchemy import exc
from model import RentalModel

app = Flask(__name__)


RentalDB.init_app(app)
migrate = Migrate(app)

port = os.environ.get('PORT')
if port is None:
    port = 8060

@app.errorhandler(404)

@app.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route("api/v1/rental/<string:rentalUid>", methods = ["GET"])
def get_all_rentals_user(rental_uid):
    """Получить информацию о всех арендах пользователя"""
    result=RentalDB.session.query(RentalModel).filter(RentalModel.rental_uid==rental_uid).one_or_none()
    if not result:
        abort(404)
    return make_response(jsonify(result), 200)



