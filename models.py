from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.String(1), unique=True, nullable=False)

    def __repr__(self):
        return '<ToDO %r>' % self.ToDO

def create_user(username, password):

    currentuser = User( username, password ) 

    db.session.add(currentuser)

    db.session.commit()

    return currentuser

def login_user(user_name, pass_word):
    #user = User('','')
    result = User.query.filter_by(username=user_name).first()
    if result is None:
        print('User not found')
        return False
    else:
        if result.password == pass_word:
            g.user['username'] = result.username
            return True
        else:
            return False

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")
