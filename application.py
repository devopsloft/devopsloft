import sys
import os

from flask import Flask, flash, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt

application = Flask(__name__)

# Config MySQL
application.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'mysql')
application.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'application')
application.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'application')
application.config['MYSQL_DB'] = 'devopsloft'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'
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
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
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

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) \
            VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now signed up', 'success')

        return(redirect(url_for('home')))
    return render_template('signup.html', form=form)


@application.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    application.secret_key = 'secret123'
    application.run(debug=True, host='0.0.0.0', port=5000)
