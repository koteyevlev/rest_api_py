from app import app
from flask import Flask, jsonify, render_template, request
import json
import flask
import re
import datetime
from models import Citizen
from app import db
import numpy as np


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

    return json_s, errors


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


def argv_valid(cit, relatives_check, unique_cit_id):
    if not list(set(relatives_check)) == relatives_check:
        return 1
    if cit["citizen_id"] in unique_cit_id or int(cit['citizen_id']) < 0:
        return 1
    if len(cit['town']) > 256 or cit["town"] == "" or not re.search('[a-zA-Z0-9]', cit['town']):
        return 1
    if len(cit['street']) > 256 or cit["street"] == "" or not re.search('[a-zA-Z0-9]', cit['street']):
        return 1
    if len(cit['building']) > 256 or cit["building"] == "" or not re.search('[a-zA-Z0-9]', cit['building']):
        return 1
    if len(cit['name']) > 256 or cit["name"] == "":
        return 1
    if not cit['gender'] == 'male' and not cit['gender'] == 'female':
        return 1
    if int(cit['apartment']) < 0:
        return 1


def last_valid(errors, lst_cit, import_id):
    try:
        unique_cit_id = {}
        for cit in lst_cit:
            relatives_check = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            if not relatives_check:
                return None
            if argv_valid(cit, relatives_check, unique_cit_id):
                return 1
            unique_cit_id.add(cit['citizen_id'])
            for one in relatives_check:
                old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == one).first_or_404()
                #print(old_citizen.name, one)
                if int(cit['citizen_id']) not in list(old_citizen.relatives):
                    #print(cit['citizen_id'], old_citizen.relatives, old_citizen.name)
                    return 1
    except:
        return 1


def print_citizen(self):
    citizen = dict()
    citizen["citizen_id"] = self.citizen_id
    citizen["town"] = self.town
    citizen["street"] = self.street
    citizen["building"] = self.building
    citizen["apartment"] = self.apartment
    citizen["name"] = self.name
    citizen["birth_date"] = self.birth_date
    citizen["gender"] = self.gender
    citizen["relatives"] = self.relatives
    return citizen


@app.route('/imports', methods=["POST"])
def post_data():
#    return render_template('404.html'), 404
    json_s, errors = first_validate()
    lst_cit = json_s['citizens']
    try:
        import_id = (Citizen.query.all()[-1]).import_id + 1
    except:
        import_id = 1
    #check relatives
    if errors:
        return errors, 400
    try:
        db.create_all()
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
            if datetime.datetime.now().date() < birth_date:
                return render_template('400.html'), 400
            gender = cit['gender']
            if len(str(cit['relatives'])) > 2:
            	relatives = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            else:
                relatives = []
            # return "stupid citizens crash again"
            citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                              apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                              relatives=relatives, import_id=import_id)
            # return "Base crush"
            db.session.add(citizen)
        if last_valid(errors, lst_cit, import_id):
            return render_template('400.html'), 400
        #return render_template('400.html'), 403
        db.session.commit()
        #return "something"
        return jsonify( {"data": {"import_id": citizen.import_id}}), 201
    except:
        return render_template('400.html'), 400


@app.route('/imports/<import_id>/citizens')
def get_citizens(import_id):
    try:
        data = Citizen.query.filter(Citizen.import_id == int(import_id))
        output = {"data": []}
        for citizen in data:
            output["data"].append(citizen)
        if not output["data"]:
            return render_template('400.html'), 400
        return str(output), 200 # dont forget to create dict
    except:
        return render_template('400.html'), 400


@app.route('/imports/<import_id>/citizens/birthdays')
def get_birthdays(import_id):
    output = dict()
    month = 1
    data = Citizen.query.filter(Citizen.import_id == int(import_id))
    while month < 13:
        people = []
        output[str(month)] = []
        for citizen in data:
            if int(citizen.birth_date.strftime("%m")) == month:
                for i in citizen.relatives:
                    if i not in people:
                        output[str(month)].append({"citizen_id": i, "presents": 1})
                    else:
                        for part in output[str(month)]:
                            if part["citizen_id"] == i:
                                part["presents"] += 1
                                break
                    people.append(i)
        month += 1
        # do something
    return {"data": output}


@app.route('/imports/<import_id>/towns/stat/percentile/age')
def get_stat(import_id):
    output = []
    data = Citizen.query.filter(Citizen.import_id == int(import_id))
    towns = set()
    for one in data:
        towns.add(one.town)
    for town in towns:
        elem = dict()
        elem["town"] = town
        birth_date_data = list(Citizen.query.filter(Citizen.import_id == int(import_id)).filter(Citizen.town == town))
        tmp_ages = list()
        for i in birth_date_data:
            tmp_ages.append(((datetime.datetime.now() - i.birth_date).days / 365))
        elem["p50"] = np.round(np.percentile(tmp_ages, 50, interpolation='linear'), 2)
        elem["p75"] = np.round(np.percentile(tmp_ages, 75, interpolation='linear'), 2)
        elem["p99"] = np.round(np.percentile(tmp_ages, 99, interpolation='linear'), 2)
        output.append(elem)
    return {"data": output}


def change_relative(old_data, new_data, import_id):
    try:
        delete_list = list(set(old_data) - set(new_data))
        add_list = list(set(new_data) - set(old_data))
        if delete_list:
            for one in delete_list:
                old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == int(one)).first_or_404()
                tmp = list(old_citizen.relatives)
                tmp.remove(int(one))
                old_citizen.relatives = tmp
                if old_citizen.citizen_id == 2:
                    old_citizen.street = " Let s go"
                db.session.add(old_citizen)
        if add_list:
            for one in add_list:
                old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == int(one)).first_or_404()
                tmp = list(old_citizen.relatives)
                if int(one) not in tmp:
                    tmp.append(int(one))
                old_citizen.relatives = tmp
    except:
        return render_template('400.html'), 400


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=["PATCH"])
def edit_data(import_id, citizen_id):
    try:
        old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == citizen_id).first_or_404()
        json_s = flask.request.get_json()
        if json_s is None:
            return render_template('400.html'), 400
        editors = json_s.keys()
        for line in editors:
            if line not in ['town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']:
                return render_template('400.html'), 400
        citizen_id, town, street, building, apartment, name, birth_date, gender, relatives, import_id = old_citizen.citizen_id, old_citizen.town, old_citizen.street, old_citizen.building, old_citizen.apartment, old_citizen.name, old_citizen.birth_date, old_citizen.gender, old_citizen.relatives, old_citizen.import_id
        cit = json_s
        if not cit['town'] is None:
            old_citizen.town = cit['town']
        if not cit['street'] is None:
            old_citizen.street = cit['street']
        if not cit['building'] is None:
            old_citizen.building = cit['building']
        if not cit['apartment'] is None:
            old_citizen.apartment = cit['apartment']
        if not cit['name'] is None:
            old_citizen.name = cit['name']
        if not cit['birth_date'] is None:
            old_citizen.birth_date = datetime.datetime.strptime(cit['birth_date'], '%d.%m.%Y').date()
        if datetime.datetime.now().date() < old_citizen.birth_date:
            return render_template('400.html'), 400
        if not cit['gender'] is None:
            old_citizen.gender = cit['gender'] # check gender
        if not cit['relatives'] is None:
            try:
                new_data = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            except:
                new_data = []
            if change_relative(old_citizen.relatives, new_data, import_id) or \
                    argv_valid({"town": town, "street": street, "building": building, "apartment": apartment, "name": name, "gender": gender, "citizen_id": citizen_id}, old_citizen.relative, {}):
                return "Problem with arguments", 400
            old_citizen.relatives = new_data
        db.session.commit()
        printer = print_citizen(old_citizen)
        return ({"data": printer}) # порядок неверный
    except:
        return render_template('400.html'), 400
