from wtforms import Form, BooleanField, StringField, PasswordField, validators

class SubscribeForm(Form):
    firstName = StringField('First Name', [validators.Length(min=4, max=25)])
    lastName = StringField('Last Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    expertise = StringField('Expertise', [validators.Length(min=6, max=35)])
