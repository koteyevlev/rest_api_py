from app import app
from flask import Flask, jsonify, render_template
import json
import flask
from app import db


def first_validate():
    errors = []
    json_s = flask.request.get_json()
    if json_s is None:
        errors.append(
            "No json sent. Please sent some data to post")
        return None, errors

    for field_name in ['title', 'url']:
        if type(json_s.get(field_name)) is not str:
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


@app.route('/imports', method=["POST"])
def post_data():
    json_s, errors = first_validate()
    #errors= last_valid(errors)
    if errors:
        return flask.Response(status=400), 400
    db.create_all()
    return json
