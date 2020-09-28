#!/usr/bin/env python3
import os
import subprocess

import boto3
import click
import dotenv
from botocore.exceptions import ClientError


def restore_certificate(server_name):
    try:
        del os.environ['AWS_PROFILE']
    except KeyError as e:
        print(f"Key {e} not found")
    client = boto3.client('s3')
    restored = True
    for key in ["cert.pem", "fullchain.pem", "privkey.pem"]:
        try:
            client.download_file(
                Bucket=os.environ['AWS_S3_BUCKET'],
                Key=key,
                Filename=f"/etc/letsencrypt/live/{server_name}/{key}"
            )
            print(f"Restoring {key}: restord")
        except ClientError:
            print(f"Restoring {key}: not found")
            restored = False
    return restored


def backup_certificate(server_name):
    try:
        del os.environ['AWS_PROFILE']
    except KeyError as e:
        print(f"Key {e} not found")
    client = boto3.client('s3')
    for key in ["cert.pem", "fullchain.pem", "privkey.pem"]:
        try:
            client.upload_file(
                Filename=f"/etc/letsencrypt/live/{server_name}/{key}",
                Bucket=os.environ['AWS_S3_BUCKET'],
                Key=key
            )
            print(f"Restoring {key}: backedup")
        except ClientError as e:
            print(e)


@ click.command()
@ click.option("-s", "--server_name", required=False, default="stage")
def main(server_name):
    dotenv.load_dotenv()
    if not restore_certificate(server_name):
        try:
            command = f"rm -Rf /etc/letsencrypt/live/{server_name}"
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            print('Error: {}.'.format(e.output))
        try:
            command = "certbot certonly -n --webroot -w /var/www/certbot " \
                "{0} --email {1} -d {2} --rsa-key-size 4096 " \
                "--agree-tos".format(
                    "--staging" if server_name != "www.devopsloft.io" else "",
                    os.getenv("EMAIL"),
                    server_name
                )
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            print("certbot certonly")
            backup_certificate(server_name)
        except subprocess.CalledProcessError as e:
            print('Error: {}.'.format(e.output))
            raise


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
