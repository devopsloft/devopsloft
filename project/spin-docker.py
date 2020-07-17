#!/usr/bin/env python3
import logging
import os
import subprocess
from time import sleep

import boto3
import click
import dotenv


def bootstrap(environment, action, envVars):
    command = 'ecs-cli configure --cluster devopsloft '\
        '--default-launch-type EC2 --config-name default --region {0}'.format(
                os.getenv('REGION')
        )
    subprocess.run(
        command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    try:
        command = 'ecs-cli up --keypair {0} --capability-iam --size 1 '\
            '--instance-type {1} --security-group {2} --subnets {3} '\
            '--vpc {4} --aws-profile {5} --force'.format(
                os.getenv('KEYPAIR_NAME'),
                os.getenv('INSTANCE_TYPE'),
                os.getenv('SECURITY_GROUPS'),
                os.getenv('SUBNETS'),
                os.getenv('VPC'),
                os.getenv('AWS_PROFILE')
            )
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
        command = 'ecs-cli compose --ecs-params ecs-params.yml create '\
            '--region {0} --aws-profile {1} '\
            '--cluster devopsloft --launch-type EC2'.format(
                os.getenv('REGION'),
                os.getenv('AWS_PROFILE')
            )
        completed_response = subprocess.run(
            command,
            env=envVars,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        if os.getenv('ALLOCATION_ID'):
            session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
            client = session.client('ec2')
            response = client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running']
                    }
                ]
            )
            response = client.associate_address(
                AllocationId=os.getenv('ALLOCATION_ID'),
                InstanceId=response['Reservations'][0]['Instances'][0]['InstanceId'] # noqa
            )
        command = 'ecs-cli compose up --aws-profile {0}'.format(
            os.getenv('AWS_PROFILE')
        )
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


def getEnvVars(environmentName, action):
    dotenv.load_dotenv()
    envArray = os.environ.copy()
    if (environmentName == 'dev'):
        envArray['RUN_BY_PYTHON'] = 'yes'
        envArray['ENVIRONMENT'] = environmentName
        envArray['HOMEPATH'] = '/home'
    if (environmentName == 'stage'):
        envArray['RUN_BY_PYTHON'] = 'yes'
        envArray['ENVIRONMENT'] = environmentName
        envArray['HOMEPATH'] = '/home'
    if (environmentName == 'prod'):
        envArray['RUN_BY_PYTHON'] = 'yes'
        envArray['ENVIRONMENT'] = environmentName
        envArray['HOMEPATH'] = '/home'
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
        dotenv.load_dotenv()
        logging.info("AWS Profile - {0}".format(os.getenv('AWS_PROFILE')))
        session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
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
    envVars = getEnvVars(envVars, action)
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
        bootstrap(environment, action, envVars)
    elif action == 'destroy':
        teardown(environment, envVars)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
