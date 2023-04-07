from flask import Flask

import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "chauncey_billups_lasagna_turkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = flask_sqlalchemy

db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)


from app import routes