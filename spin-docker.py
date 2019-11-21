#!/usr/bin/env python3
import dotenv
import os
import subprocess
import click
import in_docker
from createPemFiles import SelfSignedCertificate, IsCertExist


print_debug = 'No'


def print_info(message):
    global print_debug
    if print_debug == 'yes':
        print("--- python debug ---> ", message)


def PrepareEnvironmentVars(environmentName, action):
    # Reads the .env file from the repository
    # Returns an array with all the env vars, inclduing modificatoins per env
	
    dotenv.load_dotenv()
    envArray = os.environ.copy()
    envArray['RUN_BY_PYTHON'] = 'yes'

    envArray['ENVIRONMENT'] = environmentName
    if (environmentName == 'dev'):

        envArray['WEB_HOST_PORT'] = envArray['DEV_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['DEV_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = envArray['DEV_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = envArray['DEV_WEB_GUEST_SECURE_PORT']
    return envArray


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
    if not (IsCertExist()):
        SelfSignedCertificate()
    if(action == "up"):
        command = "docker-compose up -d"
        subprocess.Popen(command, env=envVars, shell=True)
    if(action == "destroy"):
        command = "docker-compose down -v --rmi all --remove-orphans"
        subprocess.Popen(command, env=envVars, shell=True)


if __name__ == '__main__':
    main()
