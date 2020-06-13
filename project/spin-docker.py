#!/usr/bin/env python3
import logging
import os
import subprocess
from time import sleep

import boto3
import click
import dotenv

print_debug = 'No'


def print_info(message):
    global print_debug
    if print_debug == 'yes':
        print("--- python debug ---> ", message)


def spin(environment, action, envVars):
    command = 'ecs-cli configure --cluster devopsloft --default-launch-type EC2 --config-name default --region eu-west-1' # noqa
    subprocess.run(
        command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    try:
        command = 'ecs-cli up --keypair id_rsa --capability-iam --size 1 --instance-type t3.medium --security-group sg-02536f15a178e209f --subnets subnet-45d7e30d,subnet-ab6d49cd,subnet-d1bcda8b --vpc vpc-72fb100b --aws-profile stage --force' # noqa
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
    sleep(60)
    try:
        command = 'ecs-cli compose up --aws-profile dev'
        completed_response = subprocess.run(
            command,
            env=envVars,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print(completed_response.stdout)
    except subprocess.CalledProcessError as e:
        print('Error: {}.'.format(e.output))


def PrepareEnvironmentVars(environmentName, action):
    # Reads the .env file from the repository
    # Returns an array with all the env vars, inclduing modificatoins per env
    devwebsport = 'DEV_WEB_GUEST_SECURE_PORT'
    dotenv.load_dotenv()
    envArray = os.environ.copy()
    envArray['RUN_BY_PYTHON'] = 'yes'
    envArray['ENVIRONMENT'] = environmentName
    envArray['HOMEPATH'] = '/home'
    if (environmentName == 'dev'):
        envArray['WEB_HOST_PORT'] = envArray['DEV_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['DEV_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = \
            envArray['DEV_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = envArray[devwebsport]
    if (environmentName == 'stage'):
        envArray['WEB_HOST_PORT'] = envArray['STAGE_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['STAGE_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = \
            envArray['STAGE_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = envArray[devwebsport]
        envArray['AWS_S3_BUCKET'] = envArray['STAGE_AWS_S3_BUCKET']
    if (environmentName == 'prod'):
        envArray['WEB_HOST_PORT'] = envArray['PROD_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['PRDO_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = \
            envArray['PROD_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = envArray[devwebsport]
        envArray['AWS_S3_BUCKET'] = envArray['PROD_AWS_S3_BUCKET']
    return envArray


def teardown(environment='dev', envVars=[]):
    logging.info("Tearing down environment {0}".format(environment))

    if environment == 'dev':
        command = "docker-compose down -v --rmi all --remove-orphans"
        completed_response = subprocess.run(
            command,
            env=envVars,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print(completed_response.stdout)
    elif environment in ['stage', 'prod']:
        session = boto3.Session(profile_name='dev')

        client = session.client('ecs')
        clusterList = client.list_clusters()
        if clusterList['clusterArns']:
            containerInstancesList = client.list_container_instances(
                cluster=clusterList['clusterArns'][0],
                status='ACTIVE'
            )
            if containerInstancesList['containerInstanceArns']:
                response = client.deregister_container_instance(
                    cluster=clusterList['clusterArns'][0],
                    containerInstance=containerInstancesList['containerInstanceArns'][0], # noqa
                    force=True
                )

            response = client.delete_cluster(
                cluster=clusterList['clusterArns'][0]
            )

            client = session.client('cloudformation')
            response = client.list_stacks(
                StackStatusFilter=['CREATE_COMPLETE']
            )
            if response['StackSummaries']:
                response = client.delete_stack(
                    StackName=response['StackSummaries'][0]['StackId'],
                )


@click.command()
@click.option("-e", "--environment", required=False, default="dev",
                    type=click.Choice(["dev", "prod", "stage"]))
@click.option("-a", "--action", required=False, default="up",
                    type=click.Choice(["up", "destroy"]))
@click.option("-d", "--debug", required=False, default="no",
                    type=click.Choice(["yes", "no"]))
def main(environment, action, debug):
    machineName = environment
    envVars = machineName
    envVars = PrepareEnvironmentVars(envVars, action)
    if environment == 'dev' and action == "up":
        command = "docker-compose up -d"
        try:
            completed_response = subprocess.run(
                command,
                env=envVars,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            print(completed_response.stdout)
        except subprocess.CalledProcessError as e:
            print('Error: {}.'.format(e.output))
    elif environment in ['stage', 'prod'] and action == "up":
        spin(environment, action, envVars)
    elif action == 'destroy':
        teardown(environment, envVars)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
