#!/usr/bin/env python3
import os
import subprocess

import click
import dotenv


@ click.command()
@ click.option("-s", "--server_name", required=False, default="stage")
def main(server_name):
    dotenv.load_dotenv()
    try:
        command = "rm -Rf /etc/letsencrypt/live/{0}".format(server_name)
        completed_response = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print(completed_response.stdout)
    except subprocess.CalledProcessError as e:
        print('Error: {}.'.format(e.output))
    try:
        command = "certbot certonly -n --webroot -w /var/www/certbot {0} " \
            "--email {1} -d {2} --rsa-key-size 4096 " \
            "--agree-tos".format(
                "--staging" if server_name != "www.devopsloft.io" else "",
                os.getenv("EMAIL"),
                server_name
            )
        completed_response = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print('Error: {}.'.format(e.output))
        raise


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
