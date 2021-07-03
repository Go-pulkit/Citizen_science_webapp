"""
This is a project for my Codecademy Flask web apps skill path 
to demonstrate my skills in creating web applications using the Flask framework in Python. 
It is a citizen science web app called 'Bird Sight'. 
It allows people to submit various types of data on bird sightings
for understanding their distribution, population dynamics and to bring together a community of birders in general.

People need to register/login to submit data to the database.
The homepage fetches a variety of data queried from the database like total species, bird counts, no. of participants etc. 
"""
#Import the required modules from flask framework and initialize an app instance of Flask.
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
#create a secure key for app security.
app.config['SECRET_KEY'] = 'ultimatesecretencrypted'

#setup the database and connect it to our app 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bsdb.db'
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#enable authentication via the flask login module
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


from models import * 
from form import *

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

#Create endpoints for all the pages on our app and route to them via the route decorator. (This will be migrated to routes.py later)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods = ['GET', 'POST'])    
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    #Add the registration data to our database after form validation
    if form.validate_on_submit():
        username = Users.query.filter_by(name = form.name.data).first()
        mail = Users.query.filter_by(email = form.email.data).first()
        
        if username is not None:
            flash('Please use a different username.')
        elif mail is not None:
            flash('Please use a different email address.')  
        else:
            user = Users(name = form.name.data, email = form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you have been successfully registred as a citizen scientist!')
            return redirect(url_for('login')) 
    
    return render_template('register.html', template_form = form)


@app.route('/login', methods = ['GET', 'POST'])    
def login():
    #redirect to homepage if user is already logged in
    """if current_user.is_authenticated:
        return redirect(url_for('contribute'))"""
    #create an instance of login form class from forms.py
    form = LoginForm()
    #check username and password
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None or not user.check_password(form.password.data):
          flash('Invalid username or password')
          return redirect(url_for('login'))
    #on verification, redirect to next page(contribute page)
        #next_page = request.args.get('next')
    #if not next_page or url_parse(next_page).netloc != '': 
        else:
          login_user(user)
          return redirect(url_for('contribute'))  
    return render_template('login.html', template_form = form)

"""@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))"""


@app.route('/contribute', methods = ['GET', 'POST'])
@login_required
def contribute():
    user = current_user
    load_user(user.id)
    if user.is_authenticated:
      flash('Welcome! Ready to make a contribution? Enter your data in the form below:')  
      user = Users.query.filter_by(name = user.name).first()
      contributions = Sight.query.filter_by(user_id = user.id)
      if contributions is None:
        contributions = []
      form = Contribute()
    
      if request.method == 'POST' and form.validate():
        new_contribution = Sight(place = form.place.data, count = form.count.data, time = form.time_of_day.data, common_name = form.species.data)
        db.session.add(new_contribution)
        db.session.commit()
        flash('Thank you for your contribution!')
      else:
        flash('Please check for any errors in your submission and resubmit.')
    
    return render_template('contribute.html', template_user = user, template_contributions = contributions, template_form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))