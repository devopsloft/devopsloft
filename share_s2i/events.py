#!/usr/bin/env python3

import json
import meetup.api
from slacker import Slacker
import loft_hvac
import os
import requests


def getEvents(status):

    try:
        client = meetup.api.Client(loft_hvac.read_secret(apikey='Meetup'))
        events = client.GetEvents({'group_urlname': 'DevOps-Loft',
                                  'status': status})
        events = json.dumps(events.__dict__)
        events = json.loads(events)
        return events
    except meetup.exceptions.HttpUnauthorized as e:
        print("Failed connecting to Meetup. Error: {0}"
              .format(e))
        return None


def putSlack(channel='sandbox', message='Hello World', event=None):

    try:
        sc = Slacker(loft_hvac.read_secret(apikey='Slack'))

        response = sc.chat.post_message(
            channel=channel,
            text=message,
            unfurl_links=True
        )
        if response.body['ok']:
            print('success')
        else:
            print("Failed publishing to slack. Error: {0}"
                  .format(response['error']))

    except Exception as e:
        print(e)


def auth():

    with requests.Session() as session:
        API_KEY_ENV_NAME = 'MEETUP_CONSUMER_KEY'
        # API_SECRET_ENV_NAME = 'MEETUP_CONSUMER_SECRET'

        parameters = {}
        parameters['client_id'] = os.environ.get(API_KEY_ENV_NAME)
        parameters['response_type'] = 'authorize'
        parameters['redirect_uri'] = 'http://www.devopsloft.io/meetup'
        parameters['allow_redirects'] = True
        session.get(
            url="https://secure.meetup.com/oauth2/authorize",
            params=parameters,
            allow_redirects=True
        )


def main():

    auth()
    while True:
        events = getEvents(status='upcoming')
        if events is not None:
            for event in events['results']:
                event_url = event['event_url']
                if event_url.endswith('/'):
                    event_url = event_url[:-1]
                message = "New event: "+event['name']+"  <"+event_url+">"

                putSlack(message=message, channel='sandbox', event=event)
        print("Sharing....")


if __name__ == "__main__":
    main()
