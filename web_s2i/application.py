#!/usr/bin/env python3

from flask import Flask, flash, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

application = Flask(__name__)

# Config MySQL
application.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
application.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
application.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
application.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'
application.config['ENVIRONMENT'] = os.getenv('ENVIRONMENT')

# load statcounter variables for current environment
STATCODES = yaml.load(os.getenv('STATCODES'), Loader=yaml.FullLoader)
application.config['project'] = STATCODES[os.getenv('ENVIRONMENT')]['project']
application.config['security'] = \
    STATCODES[os.getenv('ENVIRONMENT')]['security']

# Init MySQL
mysql = MySQL(application)


@application.route('/')
@application.route('/home')
def home():
    return render_template('home.html')


@application.route('/resources')
def resources():
    return render_template('resources.html')


@application.route('/docslist')
def docslist():
    return render_template('docslist.html')


class SignupForm(Form):
    name = StringField('Name', [
        validators.Regexp(r'[A-Za-z\s]+',
                          message="Name may only contain alphanumeric \
                          characters and spaces"),
        validators.Length(min=1, max=50)
    ])
    email = StringField('Email', [
        validators.Email(),
        validators.Length(min=6, max=50)
    ])
    username = StringField('Username', [
        validators.Regexp(r'[A-Za-z0-9_]+',
                          message="Name may only contain alphanumeric \
                          characters"),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match'),

    ])
    confirm = PasswordField('Confirm Password')


@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        try:
            # Create cursor
            cur = mysql.connection.cursor()

            cur.execute("INSERT INTO users(name, email, username, password) \
                VALUES(%s, %s, %s, %s)", (name, email, username, password))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('You are now signed up', 'success')

        except Exception as e:
            flash("{}".format(e.args[1]), category='warning')

        return(redirect(url_for('home')))

    return render_template('signup.html', form=form)


@application.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    APP_GUEST_PORT = os.getenv('APP_GUEST_PORT')
    application.secret_key = 'secret123'
    application.run(debug=True, host='0.0.0.0', port=APP_GUEST_PORT)
