#!/usr/bin/env python
import json
import os
import requests
import meetup.api
from slackclient import SlackClient

def getSecret(service):
    fname = '.secrets.json'
    if not os.path.isfile(fname):
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


def putPost(service='Slack',message='Hello World'):

    try:
        r = requests.post(url='https://hooks.slack.com/services/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',
                          headers={"Content-type": "application/json"},
                          data={"text": "Hello, World!!!!"})
    except:
        print(r.text)

    # slack_token = getSecret(service='Slack')
    # sc = SlackClient(slack_token)
    # response = sc.api_call(
    #   "channels.info",
    #   channel="BENLPHSVA"
    # )
    # print(response)

    # response = sc.api_call(
    #   "chat.postMessage",
    #   channel="BENLPHSVA",
    #   text="Hello from Python! :tada:"
    # )
    # print(response)

def main():
    putPost(service='Slack',message='Hello Liora')

if __name__ == "__main__":
    main()
