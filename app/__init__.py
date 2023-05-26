from flask import Flask

import weaviate
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

import json


with open('settings.json') as file:
    settings_dictionary = json.load(file)


app = Flask(__name__)

app.config['SECRET_KEY'] = settings_dictionary['Flask_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = flask_sqlalchemy



db = SQLAlchemy(app)


from app import routes