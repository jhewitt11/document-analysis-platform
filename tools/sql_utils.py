from datetime import date, time
import os
import json

from models import QueryFile, GResult
from sqlalchemy import select




def upload_new_data_sql(data, db):
    '''
    Upload new data to the SQL database.

    Input : data - data dictionary from a new query

    Output : new query PK or 'failure'
    '''

    QUERY = data['query']
    DATE = data['date']
    TIME = data['time']
    QF_name = QUERY+'_'+DATE+'_'+TIME

    # check if this query is in the database
    test = QueryFile.query.filter_by(name=QF_name).first()
    if test != None:
        print(f'Error : QueryFile already exists.\n{test}')
        return 'failure'

    # add it
    QF_entry = QueryFile(name = QF_name)
    db.session.add(QF_entry)

    QUERY_PK = db.session.scalars(select(QueryFile.pk). \
                                    where(QueryFile.name == QF_name)
                    ).first()

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
            queryPK = QUERY_PK
        )
        db.session.add(GR_entry)

    db.session.commit()
    return QUERY_PK


def select_all_queries_sql(db):
    '''
    Get all QueryFile rows and return the right info as a list of tuples.

    Input : db - database

    Output : tuples - [(primarykey, query, date),...]

    '''

    stmt = select(QueryFile)
    results = db.session.execute(stmt)
    
    tuples=[]

    for result in results :
        row = result[0]

        title = row.name
        pk = row.pk

        pieces = title.split('_')
        query = pieces[0]
        date = pieces[1]

        tuples.append((pk, query, date))

    return tuples


def all_docs_from_querypk_sql(pk, db):

    '''
    Get GResult information given a QueryFile primary key.

    Inputs : 
        pk : QueryFile pk 
        db : database

    Output :
        results : tuples - [(searchIndex, title, displayLink),...]

    '''

    QF = db.session.scalars(select(QueryFile).where(QueryFile.pk == pk)
                            ).first()

    name = QF.name
    query = (name.split('_'))[0]


    results = db.session.scalars(select(GResult).where(

                GResult.query.contains(query)

        )).all()


    tuples = []
    for result in results:
        row = (result.searchIndex, result.title, result.displayLink)
        tuples.append(row)

    return tuples


def docs_from_querypk_sql(query_pk, indices, db):
    '''
    Get information from GResults by specifying query pk and indices.

    Input : query_pk - QueryFile primary key
            indices - list of searchIndex for desired GResults
            db - database

    Output : result_tup - (list(titles), list(displayLinks), list(texts))

    '''

    QF = db.session.scalars(select(QueryFile.name).where(QueryFile.pk == query_pk)
                        ).first()


    given_query = QF.split('_')[0]


    # TESTING
    print(f'\n\nQuery from provided query pk : {given_query}\nQuery PK : {query_pk}\n\n')


    titles = list(db.session.scalars(select(
                                        GResult.title,

                            ).where(
                                        GResult.query == given_query,
                                        GResult.searchIndex.in_(indices)
                            )
            ))

    displayLinks = list(db.session.scalars(select(
                                    GResult.displayLink,

                        ).where(
                                    GResult.query == given_query,
                                    GResult.searchIndex.in_(indices)
                        )
        ))

    texts = list(db.session.scalars(select(
                                    GResult.text,

                        ).where(
                                    GResult.query == given_query,
                                    GResult.searchIndex.in_(indices)
                        )
        ))

    print(f'\n\nLength of titles : {len(titles)}')
    print(f'DisplayLinks : {displayLinks}')
    print(f'Length of texts : {len(texts)}\n\n')


    result_tup = (titles, displayLinks, texts)

    return result_tup





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