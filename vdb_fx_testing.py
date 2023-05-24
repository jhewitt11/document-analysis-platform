import os
import json
import pickle

import tools
from models import QueryFile, GResult

import sqlalchemy
from sqlalchemy import select
import weaviate
import openai

from app import app, db



with app.app_context():

    qpk = 32

    #bundle = tools.create_data_bundle_weaviate(qpk, db, export = True)

    with open('data/openai/'+str(qpk)+'data_object.pkl', 'rb') as file :
        bundle = pickle.load(file)

    tools.upload_data_weaviate(bundle)