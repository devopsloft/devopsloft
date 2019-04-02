#!/usr/bin/env python3

import json
import os
import meetup.api
from slacker import Slacker


def getSecret(service, dirPath=os.curdir):
    fname = '.secrets.json'
    if not os.path.isfile(os.path.join(dirPath, fname)):
        exit
    with open(fname) as data:
        data_json = json.loads(data.read())
    if service == 'Meetup':
        return data_json['Meetup']['api_key']
    elif service == 'Slack':
        return data_json['Slack']['OAuth_Access_Token']


def getEvents(status):
    client = meetup.api.Client(getSecret(service='Meetup'))
    events = client.GetEvents({'group_urlname': 'DevOps-Loft',
                              'status': status})
    events = json.dumps(events.__dict__)
    events = json.loads(events)
    return events


def putSlack(channel='sandbox', message='Hello World', event=None):

    try:
        sc = Slacker(getSecret(service='Slack'))

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


def main():
    events = getEvents(status='upcoming')
    for event in events['results']:
        event_url = event['event_url']
        if event_url.endswith('/'):
            event_url = event_url[:-1]
        message = "New event: " + event['name'] + "  <" + event_url + ">"

        putSlack(message=message, channel='sandbox', event=event)


if __name__ == "__main__":
    main()
