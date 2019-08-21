from app import app
from flask import Flask, jsonify, render_template

from models import Post

@app.route('/')
def index():
    name = 'Ivan'
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

