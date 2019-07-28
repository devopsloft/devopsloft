#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../modules')
import loft_hvac  # noqa: E402

# This script must be run as root!
if not os.geteuid() == 0:
    sys.exit('This script must be run as root!')

load_dotenv(
    dotenv_path=os.path.dirname(os.path.abspath(__file__)) + '/../.env'
)
load_dotenv(
    dotenv_path=os.path.dirname(os.path.abspath(__file__)) + '/../.env.local',
    override=True
)

MEETUP_KEY = None
MEETUP_SECRET = None
MEETUP_REDIRECT_URI = None
SLACK_APIKEY = None

if len(sys.argv) == 2:
    ENVIRONMENT = sys.argv[1]
else:
    sys.exit()

if ENVIRONMENT == 'dev':
    MEETUP_KEY = os.getenv('DEV_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('DEV_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('DEV_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('DEV_SLACK_APIKEY')
    provider = 'virtualbox'
    AWS_S3_BUCKET = None
elif ENVIRONMENT == 'stage':
    MEETUP_KEY = os.getenv('STAGE_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('STAGE_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('STAGE_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('STAGE_SLACK_APIKEY')
    provider = 'aws'
    AWS_S3_BUCKET = os.getenv('STAGE_AWS_S3_BUCKET')
elif ENVIRONMENT == 'prod':
    MEETUP_KEY = os.getenv('PROD_MEETUP_KEY')
    MEETUP_SECRET = os.getenv('PROD_MEETUP_SECRET')
    MEETUP_REDIRECT_URI = os.getenv('PROD_MEETUP_REDIRECT_URI')
    SLACK_APIKEY = os.getenv('PROD_SLACK_APIKEY')
    provider = 'aws'
    AWS_S3_BUCKET = os.getenv('PROD_AWS_S3_BUCKET')

loft_hvac.initialize(provider=provider, bucket=AWS_S3_BUCKET)
loft_hvac.enable_secrets_engine()

loft_hvac.write_secret(
    provider=provider,
    bucket=AWS_S3_BUCKET,
    path='secret/meetup/key',
    secret=dict(key=MEETUP_KEY),
    mount_point='secret'
)

loft_hvac.write_secret(
    provider=provider,
    bucket=AWS_S3_BUCKET,
    path='secret/meetup/secret',
    secret=dict(key=MEETUP_SECRET),
    mount_point='secret'
)

loft_hvac.write_secret(
    provider=provider,
    bucket=AWS_S3_BUCKET,
    path='secret/meetup/redirect_uri',
    secret=dict(key=MEETUP_REDIRECT_URI),
    mount_point='secret'
)

loft_hvac.write_secret(
    provider=provider,
    bucket=AWS_S3_BUCKET,
    path='secret/slack/apikey',
    secret=dict(key=SLACK_APIKEY),
    mount_point='secret'
)
