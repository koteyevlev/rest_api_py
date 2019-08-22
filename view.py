from app import app
from flask import Flask, jsonify, render_template, request
import json
import flask
import re
import datetime
from models import Citizen
from app import db


def first_validate():
    errors = []
    json_s = flask.request.get_json()
    if json_s is None:
        errors.append(
            "No json sent. Please sent some data to post")
        return None, errors

    for field_name in ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']:
        if not type(json_s.get(field_name)):
            errors.append(
                "Field '{}' is missing or is not a string".format(field_name))
            print("I found this", field_name)

    return json_s, errors


@app.route('/')
def index():
#    return 'Go more'
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@app.route('/imports', methods=["POST"])
def post_data():
#    return render_template('404.html'), 404 
    json_s, errors = first_validate()
    #errors= last_valid(errors)
    if errors:
        print(errors[0])
        return errors[0], 400
        # return flask.Response(status=400), 400
#    try:
    if True == True:
        db.create_all()
        citizen_id = json_s['citizen_id']
        town = json_s['town']
        street = json_s['street']
        building = json_s['building']
        apartment = json_s['apartment']
        name = json_s['name']
        #birth_date = json_s['birth_date']
        #match = re.search(r'\d{2}-\d{2}-\d{4}', json_s['birth_date'])
        birth_date = datetime.datetime.strptime(json_s['birth_date'], '%d.%m.%Y').date()
        gender = json_s['gender']
        relatives = list(map(int, str(json_s['relatives'])[1:-1].split(',')))
        # return "stupid citizens crash again"
        citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                          apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                          relatives=relatives)
        # return "Base crush"
        db.session.add(citizen)
        db.session.commit()
        #return "something"
        return jsonify( {"data": citizen.import_id}), 201
    #except:
     #   return 'Something wrong', 400
