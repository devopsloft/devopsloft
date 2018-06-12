from wtforms import Form, StringField, validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# class SubscribeForm(Form):
#     firstName = StringField('First Name', [validators.Length(min=4, max=25)])
#     lastName = StringField('Last Name', [validators.Length(min=4, max=25)])
#     email = StringField('Email Address', [validators.Length(min=6, max=35)])
#     expertise = StringField('Expertise', [validators.Length(min=6, max=35)])

class SubscribeForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    expertise = StringField('Expertise', [validators.Length(min=6, max=35)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid mail'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


