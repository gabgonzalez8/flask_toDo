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
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, email, password ):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    complete = db.Column(db.Boolean)

    def __init__(self, userid, title, due_Date, complete ):
        self.userid = userid
        self.title = title
        self.due_date = due_Date
        self.complete = complete

    def __repr__(self):
        return '<ToDO %r>' % self.ToDO

def login_user(user_name, pass_word):
    result = User.query.filter_by(username=user_name).first()
    return result


def create_toDo( tuserid, tdescription, tdueDate, tstatus ):

    currenttoDo = ToDO( tuserid, tdescription, tdueDate, tstatus) 

    db.session.add(currenttoDo)

    db.session.commit()

    return currenttoDo


def ListAll( tuserid ):

    toDos = ToDO.query.filter_by(userid=tuserid).order_by("due_date")

    return toDos

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.drop_all()
    db.create_all()
    print("Done!")
