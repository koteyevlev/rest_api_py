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

    for field_name in ['citizens']:
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
    lst_cit = json_s['citizens']
    #errors= last_valid(errors)
    if errors:
        print(errors[0])
        return errors[0], 400
        # return flask.Response(status=400), 400
    try:
        db.create_all()
        try:
            import_id = Citizen.query.last().import_id + 1
        except:
            import_id = 1
        for cit in lst_cit:
            citizen_id = cit['citizen_id']
            town = cit['town']
            street = cit['street']
            building = cit['building']
            apartment = cit['apartment']
            name = cit['name']
            #birth_date = json_s['birth_date']
            #match = re.search(r'\d{2}-\d{2}-\d{4}', json_s['birth_date'])
            birth_date = datetime.datetime.strptime(cit['birth_date'], '%d.%m.%Y').date()
            gender = cit['gender']
            relatives = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            # return "stupid citizens crash again"
            citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                              apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                              relatives=relatives, import_id=import_id)
            # return "Base crush"
            db.session.add(citizen)
        db.session.commit()
        #return "something"
        return jsonify( {"data": {"import_id": citizen.import_id}}), 201
    except:
        return 'Something wrong', 400
