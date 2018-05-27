from flask_wtf import Form
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask import request

class RegistrationForm(Form):
    name = StringField('Private Name', [validators.Length(min=2, max=25)])
    surename = StringField('Sure Name', [validators.Length(min=2, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    ismaster = BooleanField('Are you a DevOps Master?', [validators.DataRequired()])
