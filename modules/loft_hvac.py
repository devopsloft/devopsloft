import json
import os

import boto3
import hvac

client = None
root_token = None
keys = None


def get_key(index):
    global keys
    vault_var = "/vault"
    if keys is None:
        with open(vault_var+'/keys.json') as keysfile:
            keys = json.load(keysfile)
    return keys[index]


def get_root_token():
    global root_token
    vault_var = "/vault"
    if root_token is None:
        with open(vault_var+'/root_token.txt') as tokenfile:
            root_token = tokenfile.read()
    return root_token


def initialize(provider='virtualbox', bucket=None):

    global client
    global root_token
    global keys
    vault_var = "/vault"

    if client is None:
        VAULT_ADDR = os.environ["VAULT_ADDR"]
        client = hvac.Client(url=VAULT_ADDR)

    if not client.sys.is_initialized():

        shares = 5
        threshold = 3

        result = client.sys.initialize(shares, threshold)

        root_token = result['root_token']
        keys = result['keys']

        with open(vault_var+'/keys.json', "w+") as keysfile:
            json.dump(keys, keysfile)

        with open(vault_var+'/root_token.txt', "w+") as tokenfile:
            tokenfile.write(root_token)

        if provider == 'aws':
            s3_client = boto3.client('s3')
            s3_client.upload_file(
                vault_var+'/keys.json',
                bucket,
                'keys.json'
            )
            s3_client.upload_file(
                vault_var+'/root_token.txt',
                bucket,
                'root_token.txt'
            )

    else:

        if keys is None or root_token is None:
            if provider == 'aws':
                s3_client = boto3.client('s3')
                s3_client.download_file(
                    bucket,
                    'keys.json',
                    vault_var+'/keys.json'
                )
                s3_client.download_file(
                    bucket,
                    'root_token.txt',
                    vault_var+'/root_token.txt'
                )

            with open(vault_var+'/keys.json') as keysfile:
                keys = json.load(keysfile)

            with open(vault_var+'/root_token.txt') as tokenfile:
                root_token = tokenfile.read()

        if client.token is None:
            client.token = root_token


def unseal(provider='virtualbox', bucket=None):

    initialize(provider=provider, bucket=bucket)

    if client.sys.is_sealed():
        client.sys.submit_unseal_keys(keys)


def seal(provider='virtualbox', bucket=None):

    initialize(provider=provider, bucket=bucket)

    if not client.sys.is_sealed():
        client.sys.seal()


def read_secret(provider='virtualbox', bucket=None, path='secret'):

    global client

    initialize(provider=provider, bucket=bucket)
    unseal()

    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response['data']['data']['key']


def write_secret(
        provider='virtualbox',
        bucket=None,
        path=None,
        secret=None,
        mount_point=None):

    initialize(provider=provider, bucket=bucket)
    unseal()

    client.secrets.kv.v2.create_or_update_secret(
        path=path,
        secret=secret,
        mount_point=mount_point
    )


def configure(provider='virtualbox', bucket=None):

    initialize(provider=provider, bucket=bucket)
    unseal()

    client.secrets.kv.v2.configure(
        max_versions=20,
        mount_point='secret',
    )


def enable_secrets_engine(provider='virtualbox', bucket=None):

    initialize(provider=provider, bucket=bucket)
    unseal()

    if 'secret' not in client.sys.list_mounted_secrets_engines()['data']:
        client.sys.enable_secrets_engine(
            backend_type='kv',
            path='secret',
            options=dict(version=2),
        )
