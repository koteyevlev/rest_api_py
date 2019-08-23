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


def last_valid(errors, lst_cit, import_id):
	try:
		for cit in lst_cit:
			relatives_check = list(map(int, str(cit['relatives'])[1:-1].split(',')))
			for one in relatives_check:
				old_citizen = Citizen.query.filter(Citizen.import_id == import_id and Citizen.citizen_id == one).first_or_404()
				if cit['citizen_id'] not in old_citizen.relatives:
					return render_template('400.html'), 400


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
        print(errors[0])
        return render_template('400.html'), 400
        # return flask.Response(status=400), 400
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
            relatives = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            # return "stupid citizens crash again"
            citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                              apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                              relatives=relatives, import_id=import_id)
            # return "Base crush"
            db.session.add(citizen)
		last_valid(errors, lst_cit, import_id)
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
        return str(output), 200
    except:
        return render_template('400.html'), 400


def print_citizen(self):
    citizen = {}
    citizen["citizen_id"] = self.citizen_id
    citizen["town"] = self.town
    citizen["street"] = self.street
    citizen["building"] = self.building
    citizen["apartment"] = self.apartment
    citizen["name"] = self.name
    citizen["birth_date"] = self.birth_date
    citizen["gender"] = self.gender
    citizen["relatives"]= self.relatives
    return (citizen)


def change_relative(old_data, new_data, import_id):
    delete_list = list(set(old_data) - set(new_data))
    add_list = list(set(new_data) - set(old_data))
	try:
        for one in delete_list:
	        old_citizen = Citizen.query.filter(Citizen.import_id == import_id and Citizen.citizen_id == one).first_or_404()
			old_citizen.relatives.remove(one)
			db.session.commit()
		for one in add_list:
	        old_citizen = Citizen.query.filter(Citizen.import_id == import_id and Citizen.citizen_id == one).first_or_404()
			old_citizen.relatives.add(one)
			db.session.commit()
	except:
		return render_template('400.html'), 400


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=["PATCH"])
def edit_data(import_id, citizen_id):
    try:
        old_citizen = Citizen.query.filter(Citizen.import_id == import_id and Citizen.citizen_id == citizen_id).first_or_404()
        json_s = flask.request.get_json()
        if json_s is None:
            return render_template('400.html'), 400
        editors = json_s.keys()
        #return str(editors)
        for line in editors:
            if line not in ['town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']:
                return render_template('400.html'), 400
        citizen_id, town, street, building, apartment, name, birth_date, gender, relatives, import_id = old_citizen.citizen_id, old_citizen.town, old_citizen.street, old_citizen.building, old_citizen.apartment, old_citizen.name, old_citizen.birth_date, old_citizen.gender, old_citizen.relatives, old_citizen.import_id
        cit = json_s
        if cit['town']:
            old_citizen.town = cit['town']
        if cit['street']:
            old_citizen.street = cit['street']
        if cit['building']:
            old_citizen.building = cit['building']
        if cit['apartment']:
            old_citizen.apartment = cit['apartment']
        if cit['name']:
            old_citizen.name = cit['name']
            #birth_date = json_s['birth_date']
            #match = re.search(r'\d{2}-\d{2}-\d{4}', json_s['birth_date'])
        if cit['birth_date']:
            old_citizen.birth_date = datetime.datetime.strptime(cit['birth_date'], '%d.%m.%Y').date()
        if datetime.datetime.now().date() < old_citizen.birth_date:
            return render_template('400.html'), 400
        if cit['gender']:
            old_citizen.gender = cit['gender']
        if cit['relatives']:
			change_relative(old_citizen.relatives, list(map(int, str(cit['relatives'])[1:-1].split(','))), import_id)
            old_citizen.relatives = list(map(int, str(cit['relatives'])[1:-1].split(',')))
			# delete old relatives
        db.session.commit()
        printer = print_citizen(old_citizen)
        return jsonify({"data": printer}) # порядок неверный
    except:
        return render_template('400.html'), 400
