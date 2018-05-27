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
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from register import RegistrationForm
#import gc

application = Flask(__name__)


@application.route('/')
def welcome():
    return render_template('home.html')


@application.route('/home')
def home():
    return render_template('home.html')


@application.route('/contact')
def contact():
    return render_template('contact.html')


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
       # user = User(form.name.data,form.surename.data, form.email.data,
                    # form.ismaster.data)
        # db_session.add(user)
        # c, conn = connection()
        # x = c.execute("SELECT * FROM users WHERE email = (%s)",
        #                   (thwart(email)))
        # if int(x) > 0:
        #     flash("That email is already taken, please choose another")
        #     return render_template('register.html', form=form)
        # else:
        #     c.execute("INSERT INTO users (name, surename, email, ismaster) VALUES (%s, %s, %s, %s)",
        #                   (thwart(name), thwart(surename), thwart(email), thwart("/introduction-to-python-programming/")))
        #     conn.commit()
        #     flash("Thanks for registering!")
        #     c.close()
        #     conn.close()
        #     gc.collect()
        #
        #     session['logged_in'] = True
        #     session['name'] = name
        #     flash('Thanks for registering')
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@application.route('/header.html')
def header():
    return render_template('header.html')


if __name__ == "__main__":
    application.run()
