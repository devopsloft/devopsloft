#!/usr/bin/env python3
import logging
import os
import subprocess
from time import sleep

import boto3
import click
import dotenv


def exec(command, envVars) -> str:
    try:
        CompletedProcess = subprocess.run(
            command,
            env=envVars,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return CompletedProcess.stdout.rstrip()
    except subprocess.CalledProcessError as e:
        print('Error: {}.'.format(e.output))
        raise


def certbot_task(command=""):
    session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
    client = session.client("ecs")
    taskDefinition = "sidecar"
    print("ECS register sidecar task")
    client.register_task_definition(
        family=taskDefinition,
        taskRoleArn="AmazonECSTaskRole",
        containerDefinitions=[
            {
                "name": "certbot",
                "image": "/".join([
                    os.getenv("NAMESPACE", default="devopsloft"),
                    "certbot:latest"
                ]),
                "essential": True,
                "command": command,
                "memory": 128,
                "mountPoints": [
                    {
                        "readOnly": False,
                        "containerPath": "/etc/letsencrypt",
                        "sourceVolume": "certs"
                    },
                    {
                        "readOnly": False,
                        "containerPath": "/var/www/certbot",
                        "sourceVolume": "www"
                    }
                ],
            }
        ],
        volumes=[
            {
                "name": "certs",
                "dockerVolumeConfiguration": {
                    "autoprovision": True,
                    "scope": "shared",
                    "driver": "local",
                }
            },
            {
                "name": "www",
                "dockerVolumeConfiguration": {
                    "autoprovision": True,
                    "scope": "shared",
                    "driver": "local",
                }
            }
        ]
    )
    print("ECS run sidecar task")

    containerInstances = client.list_container_instances(
        cluster="devopsloft",
        status="ACTIVE"
    )
    if containerInstances["containerInstanceArns"]:
        client.start_task(
            cluster="devopsloft",
            containerInstances=[
                containerInstances["containerInstanceArns"][0],
            ],
            taskDefinition=taskDefinition
        )
    else:
        raise Exception("Container Instance was not found")
    print("ECS wait untill sidecar task is stopped")
    waiter = client.get_waiter('tasks_stopped')
    tasksList = client.list_tasks(
        cluster='devopsloft',
        family=taskDefinition,
        desiredStatus='RUNNING'
    )
    if tasksList['taskArns']:
        waiter.wait(
            cluster='devopsloft',
            tasks=[
                tasksList['taskArns'][0],
            ]
        )


def bootstrap(environment, envVars):
    if environment in ["dev", "ci"]:
        exec(
            "docker run --rm --name certbot -v certs:/etc/letsencrypt "
            "-v www:/var/www/certbot {0}/certbot:latest "
            "./generateCerts.py --server_name {1}".format(
                os.getenv('NAMESPACE'),
                os.getenv('SERVER_NAME')
            ),
            envVars
        )
        if environment == "dev":
            envVars['AWS_ACCESS_KEY_ID'] = exec(
                "aws configure get aws_access_key_id --profile dev",
                envVars
            )
            envVars['AWS_SECRET_ACCESS_KEY'] = exec(
                "aws configure get aws_secret_access_key --profile dev",
                envVars
            )
        else:
            envVars['AWS_ACCESS_KEY_ID'] = 'dummy'
            envVars['AWS_SECRET_ACCESS_KEY'] = 'dummy'
        exec("docker-compose up -d", envVars)
    else:
        print("ECS cluster configuration")
        exec(
            "ecs-cli configure --cluster devopsloft "
            "--default-launch-type EC2 --config-name default "
            "--region {0}".format(
                os.getenv("AWS_DEFAULT_REGION")
            ),
            envVars
        )
        print("ECS cluster up")
        exec(
            "ecs-cli up --keypair {0} --capability-iam --size 1 "
            "--instance-type {1} --security-group {2} --subnets {3} "
            "--vpc {4} --aws-profile {5} --force".format(
                os.getenv("KEYPAIR_NAME"),
                os.getenv("INSTANCE_TYPE"),
                os.getenv("SECURITY_GROUPS"),
                os.getenv("SUBNETS"),
                os.getenv("VPC"),
                os.getenv("AWS_PROFILE")
            ),
            envVars
        )
        sleep(60)
        certbot_task(
            command=[
                "./generateCerts.py",
                "--server_name",
                os.getenv('SERVER_NAME')
            ]
        )
        print("ECS create task from compose")
        exec(
            "ecs-cli compose --project-name devopsloft "
            "--task-role-arn AmazonECSTaskRole --ecs-params ecs-params.yml "
            "create --region {0} --aws-profile {1} --cluster devopsloft "
            "--launch-type EC2".format(
                os.getenv("AWS_DEFAULT_REGION"),
                os.getenv("AWS_PROFILE")
            ),
            envVars
        )
        if os.getenv("ALLOCATION_ID"):
            session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
            client = session.client("ec2")
            response = client.describe_instances(
                Filters=[
                    {
                        "Name": "instance-state-name",
                        "Values": ["running"]
                    }
                ]
            )
            response = client.associate_address(
                AllocationId=os.getenv("ALLOCATION_ID"),
                InstanceId=response["Reservations"][0]["Instances"][0][
                    "InstanceId"
                ]
            )
        print("ECS run compose task")
        exec(
            "ecs-cli compose --project-name devopsloft "
            "--task-role-arn AmazonECSTaskRole up --aws-profile {0}".format(
                os.getenv("AWS_PROFILE")
            ),
            envVars
        )
        certbot_task(
            command=[
                "./init-letsencrypt.py",
                "--server_name",
                os.getenv('SERVER_NAME')
            ]
        )
        session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
        client = session.client("ecs")
        tasksList = client.list_tasks(
            cluster='devopsloft',
            family='devopsloft',
            desiredStatus='RUNNING'
        )
        if tasksList['taskArns']:
            print("ECS stop devopsloft task")
            client.stop_task(
                cluster='devopsloft',
                task=tasksList['taskArns'][0]
            )
            print("ECS start devopsloft task")
            client.start_task(
                cluster='devopsloft',
                containerInstances=[
                    client.list_container_instances(
                        cluster="devopsloft",
                        status="ACTIVE"
                    )["containerInstanceArns"][0],
                ],
                taskDefinition='devopsloft'
            )


def getEnvVars():
    dotenv.load_dotenv()
    envVars = os.environ.copy()
    envVars["RUN_BY_PYTHON"] = "yes"
    envVars["HOMEPATH"] = "/home"
    return envVars


def teardown(environment="dev", envVars=[]):
    logging.info("Tearing down environment {0}".format(environment))

    if environment == "dev":
        exec("docker-compose down -v --rmi all --remove-orphans", envVars)
    elif environment in ["stage", "prod"]:
        dotenv.load_dotenv()
        logging.info("AWS Profile - {0}".format(os.getenv("AWS_PROFILE")))
        session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
        client = session.client("ecs")
        clusterList = client.list_clusters()
        if clusterList["clusterArns"]:
            containerInstancesList = client.list_container_instances(
                cluster=clusterList["clusterArns"][0],
                status="ACTIVE"
            )
            if containerInstancesList["containerInstanceArns"]:
                response = client.deregister_container_instance(
                    cluster=clusterList["clusterArns"][0],
                    containerInstance=containerInstancesList[
                        "containerInstanceArns"
                    ][0],
                    force=True
                )

            response = client.delete_cluster(
                cluster=clusterList["clusterArns"][0]
            )

            client = session.client("cloudformation")
            response = client.list_stacks(
                StackStatusFilter=["CREATE_COMPLETE"]
            )
            if response["StackSummaries"]:
                response = client.delete_stack(
                    StackName=response["StackSummaries"][0]["StackId"],
                )


@ click.command()
@ click.option("-e", "--environment", required=False, default="dev",
               type=click.Choice(["dev", "ci", "prod", "stage"]))
@ click.option("-a", "--action", required=False, default="up",
               type=click.Choice(["up", "destroy"]))
def main(environment, action):
    envVars = getEnvVars()
    if action == "up":
        bootstrap(environment, envVars)
    elif action == "destroy":
        teardown(environment, envVars)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
