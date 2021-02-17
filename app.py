from flask import Flask, redirect, url_for, render_template, request, session, g, flash
from models import db,User
from models import create_user, login_user, ListAll,create_toDo, ToDO
import datetime
from forms import RegistrationForm

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

    user = login_user(user_name, user_pwd)
    if user is not None:
        if user.password == user_pwd:
            session['userid']= user.id
            session['username'] = user.username
            g.user = user
            return redirect(url_for('ToDOListAll'))
        else:
            flash('Invalid Credentials....')

    else:
        flash('Invalid Credentials....')

    return render_template('/auth/login.html' )    

@app.route("/auth/logout/")
def logout():

    g.user=None
    session.pop('username',None)
    session.pop('userid', None)

    return redirect(url_for('index'))

@app.route("/auth/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
    
    return render_template('/auth/register.html', form=form)   

@app.route("/ToDo/ListAll")
def ToDOListAll():

    if session['userid']:
        toDo_userId = session['userid']
        toDo_description = request.form.get
        toDos = ListAll( toDo_userId )

    return render_template('/ToDo/ListAll.html',toDos = toDos)

@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'GET':
        return render_template('/ToDo/add.html')

    toDo_userId = session['userid']
    toDo_title = request.form.get('description')
    date_due = request.form.get('due_Date')
    y, m, d = date_due.split('-')
    toDo_due_date = datetime.datetime(int(y), int(m), int(d))
    todo_Complete = False

    toDo = create_toDo( toDo_userId, toDo_title,  toDo_due_date, todo_Complete )

    return redirect(url_for('ToDOListAll'))

@app.route('/delete/<int:toDoiD>' )
def delete_toDo( toDoiD ):

    toDo = ToDO.query.get_or_404( toDoiD )
    db.session.delete( toDo )
    db.session.commit()

    return redirect(url_for('ToDOListAll'))

@app.route('/update/<int:toDoiD>' )
def update_toDo( toDoiD ):

    toDo = ToDO.query.get_or_404( toDoiD )
    toDo.complete = not toDo.complete
    db.session.commit()
 
    return redirect(url_for('ToDOListAll'))

if __name__ == "__main__":
    app.run(port=3000)
