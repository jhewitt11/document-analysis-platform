from .models import QueryFile, GResult

#from app import app #, db

from datetime import date, time
import os
import json

db = SQLAlchemy(app)



def upload_new_data(data, db):

    QUERY = data['query']
    DATE = data['date']
    TIME = data['time']

    QF_name = QUERY+'_'+DATE+'_'+TIME

    # check if this query is in the database
    test = QueryFile.query.filter_by(name=QF_name).first()
    if test != None:
        print(f'Error : QueryFile already exists.\n{test}')

    RESULTS = data['results']
    for result in RESULTS:

        TITLE = result['title']
        LINK = result['link']
        DISPLAYLINK = result['displayLink']
        TEXT = result['text']
        INDEX = result['index']

        # turn date into python date type
        py_date = date.fromisoformat(DATE)

        # turn time into python time type
        time_split = [int(x) for x in TIME.split('-')]
        hour = time_split[0]
        minute = time_split[1]
        second = time_split[2]

        py_time = time(hour, minute, second)

        GR_entry = GResult( 
            query = QUERY,
            date = py_date,
            time = py_time,
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
    db.session.commit()

    return



'''
This can be run as a script to update the database with all files stored in the given directory.

with app.app_context():

    file_names = os.listdir('./data')[1:]

    for file in file_names :
        
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

            # turn date into python date type
            py_date = date.fromisoformat(DATE)

            # turn time into python time type
            time_split = [int(x) for x in TIME.split('-')]
            hour = time_split[0]
            minute = time_split[1]
            second = time_split[2]

            py_time = time(hour, minute, second)

            GR_entry = GResult( 
                            query = QUERY,
                            date = py_date,
                            time = py_time,
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
        db.session.commit()

'''