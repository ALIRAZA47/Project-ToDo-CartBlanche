import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# DB Models

# User Model
class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return "<User %r>" % self.email


# 'ToDo' Model
class todo(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(300), nullable=False)
    labels = db.Column(db.String(300), nullable=True)
    username = db.Column(db.String(80), nullable=False)

    def __init__(self, title: str, priority: str, labels: str, username: str):
        self.title = title
        self.priority = priority
        self.username = username
        self.labels = labels

    def remove_todo(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<ToDo %r>" % self.title


class todo_python:
    def __init__(self, todo_id: int, title: str, priority: str, labels: list, username: str):
        self.todo_id = todo_id
        self.title = title
        self.priority = priority
        self.username = username
        self.labels = labels


# # Lables Model
# class Label(db.Model):
#     label_id = db.Column(db.Integer, primary_key=True)
#     label_name = db.Column(db.String(80), nullable=False)
#     todo_id = db.Column(db.Integer, db.ForeignKey('todo.todo_id'))
#     todo = db.relationship('ToDo', backref=db.backref('labels', lazy=True))
#
#     def __init__(self, label_name: str, todo_id: int):
#         self.label_name = label_name
#         self.todo_id = todo_id
#
#     def __repr__(self) -> str:
#         return "<Label %r>" % self.label_name
