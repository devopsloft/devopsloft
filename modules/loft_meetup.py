import requests
import sys
import os


def auth():
    with requests.Session() as session:
        parameters = {}
        parameters['client_id'] = os.getenv('CLIENT_ID_ENV_NAME')
        parameters['response_type'] = 'code'
        parameters['redirect_uri'] = os.getenv('REDIRECT_URL_ENV_NAME')

        response = session.get(
            url="https://secure.meetup.com/oauth2/authorize",
            params=parameters
        )

        return(response.content)


def get_token(code):

    with requests.Session() as session:
        parameters = {}
        parameters['client_id'] = os.getenv('CLIENT_ID_ENV_NAME')
        parameters['client_secret'] = os.getenv('CLIENT_SECRET_ENV_NAME')
        parameters['grant_type'] = 'anonymous_code'
        parameters['redirect_uri'] = os.getenv('REDIRECT_URL_ENV_NAME')
        parameters['code'] = code

        response = session.post(
            url="https://secure.meetup.com/oauth2/access",
            params=parameters
        )

        print(response.content, file=sys.stdout)
        sys.stdout.flush()
