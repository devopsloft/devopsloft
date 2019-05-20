#!/usr/bin/env python3

from dotenv import load_dotenv
import loft_hvac
import os

MEETUP_KEY = None
MEETUP_SECRET = None
MEETUP_REDIRECT_URI = None
SLACK_APIKEY = None
ENVIRONMENT = os.getenv('ENVIRONMENT')
BASE_FOLDER = os.getenv('BASE_FOLDER')

load_dotenv(dotenv_path=BASE_FOLDER + '/.env.local')

if ENVIRONMENT == 'dev':
    MEETUP_KEY = os.getenv('DEV_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('DEV_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('DEV_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('DEV_SLACK_APIKEY')
elif ENVIRONMENT == 'stage':
    MEETUP_KEY = os.getenv('STAGE_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('STAGE_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('STAGE_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('STAGE_SLACK_APIKEY')
elif ENVIRONMENT == 'prod':
    MEETUP_KEY = os.getenv('PROD_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('PROD_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('PROD_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('PROD_SLACK_APIKEY')

loft_hvac.initialize()
loft_hvac.enable_secrets_engine()

loft_hvac.write_secret(
    path='secret/meetup/key',
    secret=dict(key=MEETUP_KEY),
    mount_point='secret'
)

loft_hvac.write_secret(
    path='secret/meetup/secret',
    secret=dict(key=MEETUP_SECRET),
    mount_point='secret'
)

loft_hvac.write_secret(
    path='secret/meetup/redirect_uri',
    secret=dict(key=MEETUP_REDIRECT_URI),
    mount_point='secret'
)

loft_hvac.write_secret(
    path='secret/slack/apikey',
    secret=dict(key=SLACK_APIKEY),
    mount_point='secret'
)
