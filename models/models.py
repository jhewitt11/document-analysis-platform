from app import db
from datetime import datetime

class User(db.Model):
    
    ind =           db.Column(db.Integer, primary_key=True)
    name =          db.Column(db.String(50))
    email =         db.Column(db.String(100), unique=True)
    date_joined =   db.Column(db.Date,  default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.email}>'

class QueryFile(db.Model):

    pk =        db.Column(db.Integer, primary_key=True)
    name =      db.Column(db.String(300), unique=True)

    def __repr__(self):
        return f'<File Name : {self.name}>'



class GResult(db.Model):
   
    pk =            db.Column(db.Integer, primary_key=True)
    query =         db.Column(db.String(300))
    date  =         db.Column(db.Date)
    time =          db.Column(db.Time)
    title =         db.Column(db.String(300))
    link =          db.Column(db.String(300))
    displayLink =   db.Column(db.String(300))
    text =          db.Column(db.Text())
    searchIndex =   db.Column(db.Integer)

    def __repr__(self):
        return f'<Title : {self.title}, DisplayLink : {self.displayLink}, Index : {self.searchIndex}>'