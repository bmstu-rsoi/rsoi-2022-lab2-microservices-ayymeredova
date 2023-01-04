from email import message
import os 
import sys
from marshmallow import ValidationError
# import psycopg2
from flask import Flask, request, flash, redirect
import requests

# from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, url_for
# from flask_sqlalchemy import SQLAlchemy
# from carsDB import CarDB
# from utils import make_data_response, make_empty
from flask import send_from_directory, jsonify, make_response, json
# from sqlalchemy import exc
# from model import CarModel, db
import uuid
import datetime

app = Flask(__name__)

# db.init_app(app)

# migrate = Migrate(app)

port = os.environ.get('PORT')
if port is None:
    port = 8080

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



@app.route("/api/v1/rental/<string:rentalUid>", methods = ["DELETE"])
def delete_rental(rental_uid):
    pass


@app.route('/api/v1/cars/', methods=['GET'])
def get_cars():
    page = request.args.get('page', default=0, type=int)
    size = request.args.get('size', default=0, type=int)
    response = requests.get("http://cars:8070/api/v1/cars", params={'page':page, "size":size})
    return make_response(response.json(), 200)

# TODO!!!
@app.route('/api/v1/rental/<string:rentalUid>', methods=['GET'])
def get_rental(rental_uid):
    if "X-User-Name" not in request.headers.keys():
        return make_data_response(400, message="Request has not X-User-Name header!")


    page = request.args.get('page', default=0, type=int)
    size = request.args.get('size', default=0, type=int)
    response = requests.get(f"http://rental:8060/api/v1/rental/{rental_uid}", params={'page':page, "size":size})
    return make_response(response.json(), 200)







if __name__=="__main__":
    app.run(host="0.0.0.0", port=port, debug=True)