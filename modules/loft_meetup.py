import requests
import sys
import os
import loft_hvac

client_id = None
client_secret = None


def auth():

    global client_id

    if client_id is None:
        client_id = loft_hvac.read_secret(path='meetup', key='client_id')

    with requests.Session() as session:
        parameters = {}
        parameters['client_id'] = (
            client_id or os.environ.get('CLIENT_ID_ENV_NAME')
        )
        parameters['response_type'] = 'code'
        parameters['redirect_uri'] = os.getenv('REDIRECT_URL_ENV_NAME')

        response = session.get(
            url="https://secure.meetup.com/oauth2/authorize",
            params=parameters
        )

        return(response.content)


def get_token(code):

    global client_id
    global client_secret

    if client_id is None:
        client_id = loft_hvac.read_secret(path='meetup', key='client_id')

    if client_secret is None:
        client_secret = loft_hvac.read_secret(
            path='meetup',
            key='client_secret')

    with requests.Session() as session:
        parameters = {}
        parameters['client_id'] = (
            client_id or os.environ.get('CLIENT_ID_ENV_NAME')
        )
        parameters['client_secret'] = (
            client_secret or os.environ.get('CLIENT_SECRET_ENV_NAME')
        )
        parameters['grant_type'] = 'anonymous_code'
        parameters['redirect_uri'] = os.getenv('REDIRECT_URL_ENV_NAME')
        parameters['code'] = code

        response = session.post(
            url="https://secure.meetup.com/oauth2/access",
            params=parameters
        )

        print(response.content, file=sys.stdout)
        sys.stdout.flush()
