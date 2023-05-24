import os
import re
import pickle
import json
import tools


from app import app, db
from models import GResult, QueryFile


import sqlalchemy
from sqlalchemy import select

import weaviate
import openai


openai.api_key = "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"

MODEL = 'text-embedding-ada-002'
chunk_limit = 1000
chunk_overlap = 100


create = False

if create == True:
    with app.app_context():
        stmt = select(GResult)
        results = db.session.execute(stmt)

        object_dict = {}

        for i, result in enumerate(results):
            if i > 3 : break

            row = result[0]
            pk = row.pk
            queryPK = row.queryPK
            text = row.text

            chunks = tools.chunkify(text, chunk_limit, chunk_overlap, stats = True)
            result = openai.Embedding.create(input = chunks, model = MODEL)

            with open('data/openai/'+str(i)+'res.pkl', 'wb') as file:
                pickle.dump(result, file)

            data_list = result['data']

            for data in data_list :
                #pk
                #queryPK
                order = data['index']
                chunk = chunks[order]
                embedding = data['embedding']

                data_object = {
                    'text' : chunk,
                    'QueryPK' : queryPK,
                    'DocumentPK' : pk,
                    'Order' : order
                }

                object_dict[(pk, order)] = data_object, embedding

    with open('data_object.pkl', 'wb') as file :
        pickle.dump(object_dict, file)


with open('data_object.pkl', 'rb') as file:
    object_dict = pickle.load(file)

client = weaviate.Client(
    url = "http://localhost:8080",  # Replace with your endpoint
    
    additional_headers = {
        "X-OpenAI-Api-Key" : "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"
    }
)

class_name = 'Text_chunk'

with client.batch as batch :
    batch.batch_size = 50
    batch.dynamic = True

    for data_object, embedding in object_dict.values() :

        batch.add_data_object(
            data_object,
            class_name,
            vector = embedding
        )

tools.jprint(
        client.query.aggregate(class_name).with_meta_count().do()
    )