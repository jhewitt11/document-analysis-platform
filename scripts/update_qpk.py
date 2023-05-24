from app import app, db

from models import QueryFile, GResult

from sqlalchemy import select, update
from sqlalchemy import inspect

from datetime import time





with app.app_context() :
    
    inspector = inspect(db.engine)
    print(inspector.get_table_names())

    results = db.session.scalars(select(QueryFile))

    for result in results :

        query = result.name.split('_')[0]
        qtime = result.name.split('_')[2]

        time_split = [int(x) for x in qtime.split('-')]
        py_time = time(time_split[0], time_split[1], time_split[2])

        print(f'\n\nPK : {result.pk}')
        print(f'query : {query}')
        print(f'time : {time}')

        
        stmt = update(GResult).\
                    values(queryPK = result.pk).\
                    where(GResult.query == query).\
                    where(GResult.time == py_time)

        print(stmt)

        db.session.execute(stmt)
        db.session.commit()


        


    '''
        WHERE 
            title == ##splitted
            AND
            time == ##splitted

        MAKE
            GRESULT.querypk = result.pk 
    '''

