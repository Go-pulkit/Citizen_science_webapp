from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from models import Users

class RegisterForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    age = IntegerField('Age', validators = [DataRequired()])
    state = StringField('Your State', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
          
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    


class Contribute(FlaskForm):
    place = StringField('Location of sighting', validators = [DataRequired()])
    count = IntegerField('Number of individuals sighted', validators = [DataRequired()])
    time_of_day = IntegerField('Date and Time', validators = [DataRequired()])
    species = StringField('Common name of bird', validators = [DataRequired()]) 
    submit = SubmitField('Submit')
