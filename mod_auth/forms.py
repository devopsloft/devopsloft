from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import InputRequired, Email, Length


class SubscribeForm(FlaskForm):
    first_name = StringField(
        'First Name',
        [InputRequired(), validators.Length(min=4, max=25)]
        )
    last_name = StringField(
        'Last Name',
        [InputRequired(), validators.Length(min=4, max=25)]
        )
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            validators.Email(message='Invalid mail'),
            Length(max=50)]
        )
    expertise = StringField(
        'Expertise',
        [InputRequired(), validators.Length(min=6, max=35)]
        )


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class SignupForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(message='Invalid mail'),
            Length(max=50)]
        )
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(min=4, max=15)]
        )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8, max=80)]
        )
