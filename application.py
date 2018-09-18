# Copyright 2018 DevOpsLoft
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
# reader and writer modules


import csv

# import system paths
import config  # noqa: F401
import models

from flask import Flask, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user

from forms import SubscribeForm, LoginForm, SignupForm

application = Flask(__name__)
application.config.from_object('config.BaseConfig')

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

db = SQLAlchemy(application)

# Reload the user object from the user id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@application.route('/')
@application.route('/home')
def home():
    return render_template('home.html', name=current_user)

@application.route('/about')
def about():
    return render_template('about.html', name=current_user)

@application.route('/contact')
def contact():
    return render_template('contact.html', name=current_user)

@application.route('/subscribe', methods=['POST', 'GET'])
def subscribe():
    subscribe_form = SubscribeForm()

    # Checks if the form has been submited
    if subscribe_form.validate_on_submit():
        first_name = subscribe_form.first_name.data
        last_name = subscribe_form.last_name.data
        email = subscribe_form.email.data
        expertise = subscribe_form.expertise.data

        fieldnames = ['first_name', 'last_name', 'email', 'expertise']
        with open('data/mailingList.csv', 'a+') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)
            writer.writerow({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'expertise': expertise
            })
        flash('Thanks for Subscribing!', 'success')
        return redirect(url_for('home'))

    return render_template(
        'subscribe.html',
        subscribe_form=subscribe_form,
        name=current_user
        )

@application.route('/signup', methods=['POST', 'GET'])
def signup():
    signupForm = SignupForm()

    # Checks if the form has been submited
    if signupForm.validate_on_submit():
        try:
            hashed_password = generate_password_hash(
                signupForm.password.data,
                method='sha256'
                )
            new_user = models.User(
                username=signupForm.username.data,
                email=signupForm.email.data,
                password=hashed_password
                )
            db.session.add(new_user)
            db.session.commit()

            flash('You are now subscribed!', 'success')
            return redirect(url_for('home'))
        except exc.IntegrityError as e:
            print(e)
            db.session().rollback()
            flash('The email or username is already in use!', 'danger')
            return redirect(url_for('signup'))

    return render_template(
        'auth/signup.html',
        signupForm=signupForm,
        name=current_user
        )

@application.route('/login', methods=['POST', 'GET'])
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        # Looks for user in database
        user = models.User.query.filter_by(
            username=loginForm.username.data).first()
        if user:
            if check_password_hash(user.password, loginForm.password.data):
                login_user(user, remember=loginForm.remember.data)
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>'
    return render_template(
        'auth/login.html',
        loginForm=loginForm,
        name=current_user
        )

# Visible only if logged in
@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
