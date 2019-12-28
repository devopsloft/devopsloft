#!/usr/bin/env python3


from flask import Flask, flash, render_template, redirect, url_for
from flask import request, make_response, send_from_directory
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
import os
import yaml
import loft_meetup
import events
from apiUtil import apigetter

load_dotenv(
    dotenv_path='.env',
)
load_dotenv(
    dotenv_path='.env.local',
    override=True
)

application = Flask(__name__, static_folder='/static', static_url_path='')

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


def get_url_image(document, page, width=350, square=1):
    base = 'https://www.lucidchart.com/documents/image'
    width = str(width)
    square = str(square)
    return base + '/' + document + '/' + page + '/' + width + '/' + square


@application.route('/')
@application.route('/home')
def home():
    getter = apigetter()
    url = get_url_image('50f3a681-24ff-4c98-815c-94922e07b701', '0_0')
    imagepath = 'static/images/diagram.png'
    getter.save_image(url, imagepath)
    code = request.args.get("code")
    if code is not None:
        events.share(
            token=loft_meetup.get_token(
                code=code
            )
        )
    return render_template('home.html')


@application.route('/robots.txt')
@application.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(application.static_folder, request.path[1:])


@application.route('/resources')
def resources():
    return render_template('resources.html')


@application.route('/docslist')
def docslist():
    return render_template('docslist.html')


@application.route('/statistics')
def statistics():
    return render_template('statistics.html')


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


@application.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        return make_response(loft_meetup.auth())
    else:
        return render_template('share.html')


if __name__ == '__main__':
    APP_GUEST_PORT = os.getenv('APP_GUEST_PORT')
    application.secret_key = 'secret123'
    application.run(debug=True, host='0.0.0.0', port=APP_GUEST_PORT)
