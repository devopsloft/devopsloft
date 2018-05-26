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


@application.route('/register')
def register():
    return render_template('register.html')


@application.route('/header.html')
def header():
    return render_template('header.html')

if __name__ == "__main__":
    application.run()
