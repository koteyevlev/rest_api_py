from app import app
from flask import Flask, jsonify, render_template, request
import json
import flask
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
        if type(json_s.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(field_name))

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
        #return errors[0]
        return flask.Response(status=400), 400
    try:
        db.create_all()
        citizen_id = request.form['citizen_id']
        town = request.form['town']
        street = request.form['street']
        building = request.form['building']
        apartment = request.form['apartment']
        name = request.form['name']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        relatives = request.form['relatives']
        citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                          apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                          relatives=relatives)
        db.session.add(citizen)
        db.session.commit()
        return jsonify( "data" = citizen.import_id), 201
    except:
        return 'Something wrong', 400
