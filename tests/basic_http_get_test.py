import requests
from time import sleep


def test(domain, urls, allowed_failures, sleep_between_failures):
    test_succeeded = True
    for url in urls:
        response = requests.get(domain + url)
        if response.ok:
            print(f'{domain}{url} is online!')
        else:
            while (not response.ok) and (allowed_failures > 0):
                print(f'{domain}{url} is not available! trying again...')
                sleep(sleep_between_failures)
                allowed_failures -= 1
                response = requests.get(domain + url)
            if not response.ok:
                print(f'{domain}{url} is not available!')
                test_succeeded = False

    # Test homepage content
    response = requests.get(domain + '/')
    page_expected_content = '<title>DevOps Loft</title>'
    if response.text.find(page_expected_content) < 0:
        print(f'Failed to find page expected content: "{page_expected_content}", in url: "{domain}/"!')
        test_succeeded = False
    else:
        print(f'Found page expected content: "{page_expected_content}", in url: "{domain}/"!')

    return test_succeeded


if __name__ == '__main__':
    test_config = {
        'domain': 'http://localhost:80',
        'urls': ('/', '/home', '/resources', '/docslist', '/contact', '/signup'),
        'allowed_failures': 6,
        'sleep_between_failures': 5,
    }
    if not test(**test_config):
        exit(1)

