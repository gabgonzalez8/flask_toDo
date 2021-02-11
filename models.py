from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password ):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    status = db.Column(db.String(1), unique=False, nullable=False)

    def __init__(self, userid, description, due_Date, status ):
        self.userid = userid
        self.description = description
        self.due_date = due_Date
        self.status = status

    def __repr__(self):
        return '<ToDO %r>' % self.ToDO

def create_user(username, password):

    currentuser = User( username, password ) 

    db.session.add(currentuser)

    db.session.commit()

    return currentuser

def login_user(user_name, pass_word):
    result = User.query.filter_by(username=user_name).first()
    return result


def create_toDo( tuserid, tdescription, tdueDate, tstatus ):

    #date_str = '29/12/2017' # The date - 29 Dec 2017
    format_str = '%Y/%m/%d' # The format
    datetime_obj = datetime.strptime( tdueDate, format_str)
    currenttoDo = ToDO( tuserid, tdescription, datetime_obj, tstatus) 
    datetime.s

    db.session.add(currenttoDo)

    db.session.commit()

    return currenttoDo


def ListAll( tuserid ):

    toDos = ToDO.query.filter_by(userid=tuserid).all()

    return toDos

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.drop_all()
    db.create_all()
    print("Done!")
