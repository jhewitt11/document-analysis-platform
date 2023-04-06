from models import User
from app import db

#db.create_all()


print(User.query.list())