#!/usr/bin/env python3
import json
import sys

import loft_hvac
import meetup.api
from slacker import Slacker


def getEvents(token=None, status='upcoming'):

    try:
        client = meetup.api.Client(token)
        events = client.GetEvents({
            'group_urlname': 'DevOps-Loft',
            'status': status
        })
        events = json.dumps(events.__dict__)
        events = json.loads(events)
        return events
    except Exception as e:
        print("Failed connecting to Meetup. Error: {0}"
              .format(e), file=sys.stdout)
        sys.stdout.flush()
        return None


def putSlack(channel='sandbox', message='Hello World', event=None):

    try:
        sc = Slacker(loft_hvac.read_secret(path='secret/slack/apikey'))

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


def share(token=None):

    events = getEvents(token=token, status='upcoming')
    if events is not None:
        for event in events['results']:
            event_url = event['event_url']
            if event_url.endswith('/'):
                event_url = event_url[:-1]
            message = "New event: "+event['name']+"  <"+event_url+">"

            putSlack(message=message, channel='sandbox', event=event)


def main():
    print("TBD")


if __name__ == "__main__":
    main()
