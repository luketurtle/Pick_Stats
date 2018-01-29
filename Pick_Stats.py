from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pick-stats:pick-stats@localhost:3306/pick-stats'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# MODELS


class User(db.Model):
    id = (db.Column(db.Integer, primary_key=True))
    picker = (db.Column(db.String(30), unique=True))
    pick_id = db.relationship('Pick', backref='owner')

    def __init__(self, picker):
        self.picker = picker


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_number = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, pick_number, start_time, end_time, owner):
        self.pick_number = pick_number
        self.start_time = start_time
        self.end_time = end_time
        self.owner = owner


# TODO:1 Set up the rest of the classes and figure out how to get timestamps on scans.

# TODO:2 Set up @app.routes for the various pages that will be used
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/')
def display_users():
    if request.args.get('id'):
        user_id = request.args.get('id')
        all_users = User.query.get(user_id)
        return render_template('index.html', all_users=all_users)
    else:
        all_users = User.query.all()
        return render_template('index.html', all_users=all_users)

# TODO:3 Set up html pages for scanning(login.html,


if __name__ == "__main__":
    app.run()
