#!/usr/bin/env python3

import requests
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()


def http_get(uri):
    try:
        return requests.get(uri, timeout=3)
    except BaseException:
        pass
    return None


def test(domain, urls, allowed_failures, sleep_between_failures):
    test_succeeded = True
    for url in urls:
        response = http_get(domain + url)
        if not response or not response.ok:
            while (not response or not response.ok) and (allowed_failures > 0):
                print(f'{domain}{url} is not available! trying again...')
                sleep(sleep_between_failures)
                allowed_failures -= 1
                response = http_get(domain + url)
            if not response or not response.ok:
                print(f'{domain}{url} is not available!')
                test_succeeded = False
            else:
                print(f'{domain}{url} is online!')
        else:
            print(f'{domain}{url} is online!')

    # Test homepage content
    response = http_get(domain + '/')
    page_expected_content = '<title>DevOps Loft</title>'
    if not response or response.text.find(page_expected_content) < 0:
        found_output = 'Failed to find page expected content: '
        test_succeeded = False
    else:
        found_output = 'Found page expected content: '
    print(found_output + f'"{page_expected_content}", in url: "{domain}/"!')

    return test_succeeded


if __name__ == '__main__':
    urls = (
        '/',
        '/home',
        '/resources',
        '/docslist',
        '/contact',
        '/signup',
        '/share'
    )
    test_config = {
        'domain': 'http://127.0.0.1:' + os.getenv('APP_GUEST_PORT'),
        'urls': urls,
        'allowed_failures': 6,
        'sleep_between_failures': 5,
    }
    if not test(**test_config):
        exit(1)
