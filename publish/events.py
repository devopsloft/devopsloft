#!/usr/bin/env python
import json
import os
import meetup.api
from slackclient import SlackClient


def getSecret(service, dirPath=os.curdir):
    fname = '.secrets.json'
    if not os.path.isfile(os.path.join(dirPath,fname)):
        exit
    with open(fname) as data:
        data_json = json.loads(data.read())
    if service == 'Meetup':
        return data_json['Meetup']['api_key']
    elif service == 'Slack':
        return data_json['Slack']['OAuth_Access_Token']


def getEvents(status):
    events = client.GetEvents({'group_urlname': 'DevOps-Loft',
                               'status': status})
    events = json.dumps(events.__dict__)
    events = json.loads(events)
    for event in events['results']:
        print(event['name'])
    client = meetup.api.Client(getSecret(service='Meetup'))
    getEvents(status='past')


def putPost(service='Slack', channel='sandbox', message='Hello World'):
    try:
        slack_token = getSecret(service='Slack')
        sc = SlackClient(slack_token)

        response = sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=message
        )

        if response['ok']:
            print('success')
        else:
            print("Failed publishing to slack. Error: {0}".format(response['error']))

    except Exception as e:
        print(e)


def main():
    putPost(service='Slack', message='Hello Liora', channel='sandbox')


if __name__ == "__main__":
    main()
