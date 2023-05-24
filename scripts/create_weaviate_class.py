import os
import json
import weaviate
import tools

from app import app, db
from models import QueryFile, GResult
from sqlalchemy import select, update
from sqlalchemy import inspect





os.environ['OPENAI_API_KEY'] = "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"

client = weaviate.Client(
    url = "http://localhost:8080",  # Replace with your endpoint
    additional_headers = {
        "X-OpenAI-Api-Key" : "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"
    }
)

class_obj = {
    'class' : 'Text_chunk',
    'description' : 'A chunk of text from a document',

    "vectorizer": "text2vec-openai",

    "moduleConfig": {
        "text2vec-openai": {
            "model": "ada",
            "modelVersion": "002",
            "type": "text"
        }    
    },

    'properties' : [
        {
            'name': 'Text',
            'dataType' : ['text'],
            'description' : 'A chunk of text.',
        },
        {
            'name' : 'QueryPK',
            'dataType' : ['int'],
            'description' : 'Primary key of the Query associated with this chunk.'
        },
        {
            'name' : 'DocumentPK',
            'dataType' : ['int'],
            'description' : 'Primary key of the Document associated with this chunk.'
        },
        {
            'name' : 'Order',
            'dataType' : ['int'],
            'description' : 'This chunks position in the document.'
        }
    ]
}
client.schema.delete_class('text_chunk')

client.schema.create_class(class_obj)

print(f'\n\n**Schema structure **')
tools.jprint(client.schema.get(), 4)