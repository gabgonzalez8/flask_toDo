from flask import Flask, redirect, url_for, render_template, request
from models import db
from models import create_user, login_user

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

# db.create_all()

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/auth/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/auth/login.html")

    user_name = request.form.get('username')
    user_pwd = request.form.get('password')

    if login_user(user_name, user_pwd):
        return render_template('/auth/register.html')
    else:
        return render_template('/auth/login.html' )    


@app.route("/auth/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("/auth/register.html")
    user_name = request.form.get('username')
    user_pwd = request.form.get('password')

    user = create_user(user_name, user_pwd)
    return render_template('/auth/register.html', user=user)    

if __name__ == "__main__":
    app.run(port=3000)
