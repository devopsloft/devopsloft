#!/usr/bin/env python3

from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()


def http_get(uri):
    try:
        return requests.get(uri, timeout=3, verify=False)
    except BaseException:
        pass
    return None


def test(
        domain=None,
        urls=('/'),
        allowed_failures=6,
        sleep_between_failures=5,
        page_expected_content=None):
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
        'domain': 'http://127.0.0.1:80',
        'urls': urls,
        'allowed_failures': 6,
        'sleep_between_failures': 5,
        'page_expected_content': '<title>DevOps Loft</title>'
    }
    if not test(**test_config):
        exit(1)
    test_config = {
        'domain': 'https://127.0.0.1:8443',
        'urls': urls,
        'allowed_failures': 6,
        'sleep_between_failures': 5,
        'page_expected_content': '<title>DevOps Loft</title>'
    }
    if not test(**test_config):
        exit(1)
    test_config = {
        'domain': 'http://127.0.0.1:8200',
        'allowed_failures': 6,
        'sleep_between_failures': 5,
        'page_expected_content': '<title>Vault</title>'
    }
    if not test(**test_config):
        exit(1)
