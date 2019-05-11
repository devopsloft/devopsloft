import os
import json
import hvac

client = None
root_token = None
keys = None


def initialize():

    global client
    global root_token
    global keys

    if client is None:
        VAULT_ADDR = os.environ["VAULT_ADDR"]
        client = hvac.Client(url=VAULT_ADDR)

    if not client.sys.is_initialized():

        shares = 5
        threshold = 3

        result = client.sys.initialize(shares, threshold)

        root_token = result['root_token']
        keys = result['keys']

        if not os.path.isdir('/vault'):
            os.mkdir('/vault')
            print("Directory '/vault' Created")

        with open('/vault/keys.json', "w+") as keysfile:
            json.dump(keys, keysfile)

        with open('/vault/root_token.txt', "w+") as tokenfile:
            tokenfile.write(root_token)

    else:

        if keys is None:
            with open('/vault/keys.json') as keysfile:
                keys = json.load(keysfile)

        if root_token is None:
            with open('/vault/root_token.txt') as tokenfile:
                root_token = tokenfile.read()

        if client.token is None:
            client.token = root_token


def unseal():

    initialize()

    if client.sys.is_sealed():
        client.sys.submit_unseal_keys(keys)


def seal():

    initialize()

    client.sys.seal()


def read_secret(apikey):

    global client

    initialize()

    unseal()
    # response = client.secrets.kv.v2.list_secrets(
    #     path='secret/apikey/',
    #     mount_point='secret')
    # print(response)
    response = client.secrets.kv.v2.read_secret_version(
        path='secret/apikey/' + apikey,
        mount_point='secret')
    return response['data']['data']['key']


def write_secret(path, secret, mount_point):

    initialize()

    unseal()
    client.secrets.kv.v2.create_or_update_secret(
        path=path,
        secret=secret,
        mount_point=mount_point
    )


def configure():

    initialize()

    unseal()
    client.secrets.kv.v2.configure(
        max_versions=20,
        mount_point='secret',
    )


def secrets_engine():

    initialize()

    unseal()
    if 'secret/' not in client.sys.list_mounted_secrets_engines()['data']:
        client.sys.enable_secrets_engine(
            backend_type='kv',
            path='secret',
            options=dict(version=2),
        )
