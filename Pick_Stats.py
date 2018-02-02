from flask import Flask, request, render_template, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pick-stats:pick-stats@localhost:3306/pick-stats'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'PQ8v5e56rF'

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
    wave_number = db.Column(db.Integer, unique=True)
    pick_quantity = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, wave_number, start_time, end_time, owner):
        self.wave_number = wave_number
        self.start_time = start_time
        self.end_time = end_time
        self.owner = owner


# TODO:1 Figure out how to get timestamps on scans.

# TODO:2 Set up @app.routes for the various pages that will be used

@app.before_request
def require_login():
    allowed_routes = ['signup', 'login']
    if request.endpoint not in allowed_routes and 'picker' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        picker = request.form['picker']
        users = User.query.filter_by(picker=picker)
        if users.count() == 1:
            picker = users.first()
            session['picker'] = picker.picker
            flash('Welcome Back, ' + picker.picker)
            return redirect('/')
        flash("You aren't in the database. Please sign up first.")
        return render_template('login.html', picker=picker)


@app.route('/logout')
def logout():
    del session['picker']
    flash('Catch you later!')
    return redirect('login')


@app.route('/')
def display_users():
    if request.args.get('id'):
        user_id = request.args.get('id')
        all_users = User.query.get(user_id)
        return render_template('index.html', all_users=all_users)
    else:
        all_users = User.query.all()
        return render_template('index.html', all_users=all_users)


@app.route('/singlepicker')
def single_picker():
    if request.args.get('id'):
        picker_id = request.args.get('id')
        owner = User.query.get(picker_id)
        picks = Pick.query.filter_by(owner=owner).all()
        return render_template('singlepicker.html', picks=picks, owner=owner.picker)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        picker = request.form['picker']
        existing_picker = User.query.filter_by(picker=picker).first()
        if existing_picker:
            flash('Someone already has that name.')
            return redirect('/signup')
        user = User(picker=picker)
        db.session.add(user)
        db.session.commit()
        session['picker'] = user.picker
        return redirect('/')
    else:
        return render_template('signup.html')


@app.route('/pick/start', methods=['POST', 'GET'])
def pick():
    if request.method == 'GET':
        return render_template('pick.html')

    if request.method == 'POST':
        picker = User.query.filter_by(picker=session['picker']).first()
        wave_number = request.form['wave_number']
        pick_quantity = request.form['pick_quantity']
        start_time = ''
        end_time = ''
        long_pick_error = ''
        short_pick_error = ''
        pick_quantity_error = ''

        if len(wave_number) < 5:
            short_pick_error = "That pick number is too short. Please enter a valid pick number"
        if len(wave_number) > 5:
            long_pick_error = "That pick number is too long. Please enter a valid pick number"
        if len(pick_quantity) < 1:
            pick_quantity_error = "Please scan a pick quantity to continue"

        if not short_pick_error and not long_pick_error and not pick_quantity_error:
            # if len(start_time) < 1:
            # start_time = datetime.now()
            # else:
            # end_time = datetime.now()
            new_pick = Pick(wave_number, pick_quantity, start_time, end_time, picker)
            db.session.add(new_pick)
            db.session.commit()
            new_url = "/pick?id=" + str(new_pick.id)
            return redirect(new_url)
        else:
            return render_template('pick.html', short_pick_error=short_pick_error, long_pick_error=long_pick_error,
                                   pick_quantity_error=pick_quantity_error)


# TODO:3 Set up html pages for scanning(login.html,index.html,pick.html,signup.html)


if __name__ == "__main__":
    app.run()
