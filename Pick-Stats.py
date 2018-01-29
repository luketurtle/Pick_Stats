from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pickstats:pickstats@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# MODELS

class User(db.Model):
    id(db.Column(db.Integer, primary_key=True))
    name(db.Column(db.String(30), unique=True)

    def __init__(self, name):
        self.name


class Pick(db.Model):
    id(db.Column(db.Integer(10), unique=True))
# TODO:1 Set up the rest of the classes and figure out how to get timestamps on scans.

# TODO:2 Set up @app.routes for the various pages that will be used.
