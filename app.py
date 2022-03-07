# flask imports
import json

from flask import Flask, session
from flask import render_template, request
from flask import redirect, url_for
from flask import jsonify
import flash

# models import
from Models import User, todo, todo_python

# database imports
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = b'afw3rt5tfgse2453ve'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

# db initialization
db = SQLAlchemy(app)


# db.create_all()


def parseData(data):
    todo_data_python_parsed = []
    for td in data:
        todo_data_python_parsed.append(
            todo_python(td.todo_id, td.title, td.priority, td.labels.split(','), td.username))
    return todo_data_python_parsed


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():  # put application's code here
    if 'user' in session:
        return render_template('index.html', todo_data=parseData(todo.query.filter_by(username=session['user']).all()))
    else:
        return render_template('login.html')


# signup route
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # signup is a POST request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password-repeat']
        email = request.form['email']

        # print(user.username)
        if password == confirm_password:
            # flash('success', 'Password match')
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()

            # save use in session before redirecting to home page
            session['user'] = username
            return redirect(url_for('index'))

        else:
            return render_template('signup.html')
    else:
        # if a GET request is made, return the signup page
        return render_template('signup.html')


# login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    print(session)
    # validate login is a POST request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # save user's id in session before redirecting to home page
            todo_data_sql = todo.query.all()
            # print(todo_data_python_parsed[0].labels)
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    # if a GET request is made, return the login page
    else:
        if 'user' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


# delete_todo route
@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    t_id = request.form['todo_id']
    print(t_id)
    todo_to_delete = todo.query.filter_by(todo_id=t_id).first()
    print(todo_to_delete)
    todo_to_delete.remove_todo()
    # return hello_world()
    todo_data_sql = todo.query.filter_by(username=session['user']).all()
    return redirect(url_for('index'))


# add_todo route
@app.route('/add_todo', methods=['POST'])
def add_todo():
    title = request.form['title']
    priority = request.form['options-outlined']
    labels = request.form['labels']
    print(priority, title, labels)
    # breakpoint()
    todo_to_add = todo(title, priority, labels, session['user'])
    db.session.add(todo_to_add)
    db.session.commit()
    todo_data_sql = todo.query.filter_by(username=session['user']).all()
    return redirect(url_for('index'))


# update_todo route
@app.route('/update_todo', methods=['POST'])
def update_todo():
    # print("updating")
    # title = request.form['title']
    # priority = request.form['options-outlined']
    # labels = request.form['labels']
    # print("Update--->"+ title, priority, labels)
    # # breakpoint()
    # todo_to_update = todo(title,priority, labels, session['user'])
    # todo_to_update.update_todo(title, labels)
    # # todo_data_sql = todo.query.filter_by(username=session['user']).all()
    # return redirect(url_for('index'))
    return "update func in progress"


# select todo using an id
@app.route('/select_todo', methods=['POST'])
def select_todo():
    t_id = request.form['todo_id']
    todo_to_select = todo.query.filter_by(todo_id=t_id).first()
    todo_to_select = todo_to_select
    todo_dict = {
        'title': todo_to_select.title,
        'priority': todo_to_select.priority,
        'labels': todo_to_select.labels,
        'todo_id': todo_to_select.todo_id
    }
    print(todo_dict)
    return json.dumps(todo_dict)


# logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
