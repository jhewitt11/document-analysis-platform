from app import app, db

from models import QueryFile, GResult

from sqlalchemy import select, update
from sqlalchemy import inspect

from datetime import time

import tools



with app.app_context() :
    
    inspector = inspect(db.engine)
    print(inspector.get_table_names())
    print(GResult.__table__.name)

     

    results = db.session.scalars(select(GResult))

    for result in results:

        clean_text = tools.clean_text(result.text)
        pk = result.pk

        stmt = update(GResult).\
                    values(text = clean_text).\
                    where(GResult.pk == pk)


        db.session.execute(stmt)
        db.session.commit()


        