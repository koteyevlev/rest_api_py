from app import app
from flask import Flask, jsonify, render_template, request
import json
import flask
import re
import datetime
from models import Citizen, Import_id
from app import db
import numpy as np

'''
Первичная валидация проверяет был ли передан json и есть ли в нем нужныe ключи
'''

def first_validate():
    errors = []
    json_s = flask.request.get_json()
    if json_s is None:
        errors.append(
            "No json sent. Please sent some data to post\n")
        return None, errors
    editors = list(json_s)
    if not len(editors) == 1 or not editors[0] == 'citizens':
        return "Invalid key in json\n", 400
    return json_s, errors


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return "Invalid URL\n", 404


@app.errorhandler(400)
def page_not_found(e):
    return "Bad Request\n", 400

'''
Валидация аргументов проверяет соответствие аргументов требованиям указанным в таблице задания
'''


def argv_valid(cit, relatives_check, unique_cit_id):
    if not len(set(relatives_check)) == len(relatives_check):
        return 1
    if cit["citizen_id"] in unique_cit_id or int(cit['citizen_id']) < 0:
        return 1
    if len(cit['town']) > 256 or cit["town"] == "" or not re.search('[a-zA-Z0-9]', cit['town']):
        if not 0 > len(cit['town']) > 256:
            try:
                cit['town'].encode('ascii')
                return 1
            except:
                pass
        else:
            print("er town")
            return 1
    if len(cit['street']) > 256 or cit["street"] == "" or not re.search('[a-zA-Z0-9]', cit['street']):
        if not 0 > len(cit['street']) > 256:
            try:
                cit['street'].encode('ascii')
                return 1
            except:
                pass
        else:
            return 1
    if len(cit['building']) > 256 or cit["building"] == "" or not re.search('[a-zA-Z0-9]', cit['building']):
        if not 0 > len(cit['building']) > 256:
            try:
                cit['building'].encode('ascii')
                return 1
            except:
                pass
        else:
            return 1
    if len(cit['name']) > 256 or cit["name"] == "":
        return 1
    if not cit['gender'] == 'male' and not cit['gender'] == 'female':
        return 1
    if int(cit['apartment']) < 0:
        return 1


'''
До коммита все данные проверяются на уникальность citizen_id и на правильность родственных связей
'''

def last_valid(lst_cit, import_id, relat_dict):
    try:
        unique_cit_id = list()
        for cit in lst_cit:
            try:
               relatives_check = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            except:         
                if argv_valid(cit, [], unique_cit_id):
                    return 1
                unique_cit_id.append(cit['citizen_id'])
                continue
            if argv_valid(cit, relatives_check, unique_cit_id):
                 return 1
            unique_cit_id.append(cit['citizen_id'])
            for one in relatives_check:
                if one == int(cit['citizen_id']):
                    continue
                if (cit['citizen_id']) not in relat_dict[one]:
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
    citizen["birth_date"] = datetime.datetime.strftime(self.birth_date, "%d.%m.%Y")
    citizen["gender"] = self.gender
    citizen["relatives"] = self.relatives
    return citizen


'''
При реализации первого задания как и в дальнейшем была использована библиотека SQLAlchemy для работы с базой данных
Все данные сохраняются в таблицу только после валидации
'''


@app.route('/imports', methods=["POST"])
def post_data():
    json_s, errors = first_validate()
    lst_cit = json_s['citizens']
    try:
        import_id = Import_id.query.all()[-1].last_id + 1
    except:
        import_id = 1
    last_id = Import_id(last_id=import_id)
    db.session.add(last_id)
    if errors:
        return errors, 400
    try:
        db.create_all()
        relat_dict = dict()
        for cit in lst_cit:
            editors = list(cit)
            for line in editors:
                if line not in ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']:
                    return "Invalid keys in citizen\n", 404
            citizen_id = cit['citizen_id']
            town = cit['town']
            street = cit['street']
            building = cit['building']
            apartment = cit['apartment']
            name = cit['name']
            birth_date = datetime.datetime.strptime(cit['birth_date'], '%d.%m.%Y').date()
            if datetime.datetime.now().date() < birth_date:
                return "Date of some person is too large\n", 400
            gender = cit['gender']
            if len(str(cit['relatives'])) > 2:
                relatives = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            else:
                relatives = []
            citizen = Citizen(citizen_id=citizen_id, town=town, street=street, building=building,
                              apartment=apartment, name=name, birth_date=birth_date, gender=gender,
                              relatives=relatives, import_id=import_id)
            db.session.add(citizen)
            relat_dict[citizen_id] = relatives
        if last_valid(lst_cit, import_id, relat_dict):
            return "Invalid arguments\n", 400
        db.session.commit()
        return jsonify({"data": {"import_id": citizen.import_id}}), 201
    except:
        return "Bad Request\n", 400

'''
При реализации метода Get предполагалось что при несуществующем import_id надо возвращать ошибку
'''

@app.route('/imports/<import_id>/citizens')
def get_citizens(import_id):
    try:
        data = Citizen.query.filter(Citizen.import_id == int(import_id))
        output = {"data": []}
        for citizen in data:
            output["data"].append(print_citizen(citizen))
        if len(output["data"]) < 1:
            return "No such import id, check your URL\n", 400
        return output, 200 
    except:
        return "Bad Request\n", 400


'''
Алгоритм поиска подарков состоит в следующем:
1) Идет отдельная проверка каждого месяца
2) Если гражданин родился в данном месяце то все его родственники либо записываются в этот месяц 
либо если их ранее уже записали то они увеличивают число подарков на 1 в этом месяце
3) Для проверки записан ли конкретный человек в данном месяце используется отдельный лист в котором хранятся id всех
кто уже записан в таблице с подарками в данном месяце
'''


@app.route('/imports/<import_id>/citizens/birthdays')
def get_birthdays(import_id):
    output = dict()
    month = 1
    try:
        data = Citizen.query.filter(Citizen.import_id == int(import_id))
    except:
        return "Invalid import id\n", 404
    if len(list(data)) == 0:
        return "Invalid import id\n", 404
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
    return jsonify({"data": output})


'''
Статистика по городам реализуется следующим образом:
1) Создается множество всех уникальных городов в конкретном import_id
2) Для каждого элемента множество городов из базы данных выгружаются все горожане из данного города, с таким же import_id
3) Создается новый лист в который записываются возраста каждого гражданина из выгрузки
4) С помощью np.percentile и np.round из полученного листа высчитываются нужные перцентили
'''


@app.route('/imports/<import_id>/towns/stat/percentile/age')
def get_stat(import_id):
    output = []
    try:
        data = Citizen.query.filter(Citizen.import_id == int(import_id))
        if list(data) == []:
            return "No data from this import_id\n", 400
    except:
        return "Invalid import id\n", 404
    towns = list()
    for one in data:
        towns.append(one.town)
    towns = list(set(towns))
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


'''
Данная функция реализует изменение данных у родственников изменяемого гражданина если необходимо.
В частности - сначала создается список тех кому надо добавить и кому надо убрать данного гражданина,
И соответственно по этим 2 спискам из базы данных находятся необходимые граждане,
в них в дальнейшем либо удаляют либо добавляют citizen_id изменяемого гражданина в relatives
'''


def change_relative(old_data, new_data, import_id, citizen_id):
    try:
        delete_list = list(set(old_data) - set(new_data))
        add_list = list(set(new_data) - set(old_data))
        if delete_list:
            for one in delete_list:
                if int(one) == citizen_id:
                    continue
                old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == int(one)).first_or_404()
                tmp = list(old_citizen.relatives)
                tmp.remove(citizen_id)
                old_citizen.relatives = tmp
                db.session.add(old_citizen)
        if add_list:
            for one in add_list:
                if one == citizen_id:
                    continue
                old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == int(one)).first_or_404()
                tmp = list(old_citizen.relatives)
                if citizen_id not in tmp:
                    tmp.append(citizen_id)
                old_citizen.relatives = tmp
    except:
        return "Can't find some new relatives\n", 404


'''
Функция изменения данных очень похожа на функцию добавления.
Валидация данных аналогично с функцией POST
Если хоть какой то параметр невалидный то никаких изменений не произойдет
'''


@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=["PATCH"])
def edit_data(import_id, citizen_id):
    try:
        if not str(int(import_id)) == import_id or not str(int(citizen_id)) == citizen_id:
            return "Bad import_id or citizen_id", 400
        old_citizen = Citizen.query.filter(Citizen.import_id == import_id).filter(Citizen.citizen_id == citizen_id).first_or_404()
        json_s = flask.request.get_json()
        if json_s is None:
            return render_template('400.html'), 400
        editors = json_s.keys()
        if not editors:
            return "Empty json\n", 400
        for line in editors:
            if line not in ['town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']:
                return "Some keys is invalid\n", 400
        citizen_id, town, street, building, apartment, name, birth_date, gender, relatives, import_id = old_citizen.citizen_id, old_citizen.town, old_citizen.street, old_citizen.building, old_citizen.apartment, old_citizen.name, old_citizen.birth_date, old_citizen.gender, old_citizen.relatives, old_citizen.import_id
        cit = json_s
        if 'town' in cit:
            old_citizen.town = cit['town']
        if 'street' in cit:
            old_citizen.street = cit['street']
        if 'building' in cit:
            old_citizen.building = cit['building']
        if 'apartment' in cit:
            old_citizen.apartment = cit['apartment']
        if 'name' in cit:
            old_citizen.name = cit['name']
        if 'birth_date' in cit:
            old_citizen.birth_date = datetime.datetime.strptime(cit['birth_date'], '%d.%m.%Y')
        if datetime.datetime.now().date() < old_citizen.birth_date.date():
            return "Data has future date\n", 400
        if 'gender' in cit:
            old_citizen.gender = cit['gender']
        if 'relatives' in cit:
            try:
                if not cit['relatives']:
                    new_data = []
                else:
                    new_data = list(map(int, str(cit['relatives'])[1:-1].split(',')))
            except:
                return "Problem with relatives\n", 404
            to_check = {"town": old_citizen.town, "street": old_citizen.street, "building": old_citizen.building, "apartment": old_citizen.apartment, "name": old_citizen.name, "gender": old_citizen.gender, "citizen_id": citizen_id}
            if change_relative(old_citizen.relatives, new_data, import_id, citizen_id) or argv_valid(to_check, new_data, set()):
                return "Problem with arguments\n", 404
            old_citizen.relatives = new_data
        db.session.commit()
        printer = print_citizen(old_citizen)
        return ({"data": printer})
    except:
        return "Bad Request\n", 400
