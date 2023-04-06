from models import QueryFile, GResult
from app import app, db

from datetime import datetime
import os
import json


with app.app_context():

    file_names = os.listdir('./data')[1:]

    for file in file_names[:2] :
        
        with open('./data/' + file) as F:
            data = json.load(F)

        QUERY = data['query']
        DATE = data['date']
        TIME = data['time']

        QF_name = QUERY+'_'+DATE+'_'+TIME

        # check if this query is in the database
        if QueryFile.query.filter_by(name=QF_name).first() != None :
            continue

        RESULTS = data['results']
        for result in RESULTS:

            TITLE = result['title']
            LINK = result['link']
            DISPLAYLINK = result['displayLink']
            TEXT = result['text']
            INDEX = result['index']

            date_split = DATE.split('-')
            py_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))

            GR_entry = GResult( 
                            query = QUERY,
                            date = py_date,
                            time = TIME,
                            title = TITLE,
                            link = LINK,
                            displayLink = DISPLAYLINK,
                            text = TEXT,
                            searchIndex = INDEX,
                            )

            #print(GR_entry)
            db.session.add(GR_entry)

        QF_entry = QueryFile(name = QF_name)
        db.session.add(QF_entry)
