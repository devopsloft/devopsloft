#!/usr/bin/env python
import meetup.api
import json
import os


def getApiKey():
    fname = '.secrets'
    if not os.path.isfile(fname):
        exit

    with open(fname) as secret:
        api_key = secret.read().strip()
        return api_key


def getEvents(status):
    events = client.GetEvents({'group_urlname': 'DevOps-Loft',
                               'status': status})
    events = json.dumps(events.__dict__)

    events = json.loads(events)

    for event in events['results']:
        print(event['name'])


client = meetup.api.Client(getApiKey())
getEvents(status='past')
