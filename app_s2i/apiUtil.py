import requests


class apigetter:

    def __init__(self):
        pass

    def save_image(self, url, filename):
        try:
            r = requests.get(url, stream=True, verify=False)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
        finally:
            pass
