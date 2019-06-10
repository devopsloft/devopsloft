#!/usr/bin/env python3
import dotenv
import vagrant
import os
import click
from createPemFiles import SelfSignedCertificate
from createPemFiles import IsCertExist


def prepareEnvironmentVars(environementName):
    # Reads the .env file from the repository
    # Returns an array with all the env vars, inclduing modificatoins per env
    dotenv.load_dotenv()
    envArray = os.environ.copy()
    if (environementName == 'dev'):
        envArray['WEB_HOST_PORT'] = envArray['DEV_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['DEV_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = envArray['DEV_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = \
            envArray['DEV_WEB_GUEST_SECURE_PORT']
    return envArray


def startVagrant(machineName, envVars):
    # Starts a Vagrant instance with noisy logs
    # Loading the enviornement vars that was created in prepareEnvironmentVars
    vagrantInstance = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    vagrantInstance.env = envVars
    vagrantInstance.up(vm_name=machineName)


def destroyVagrant(machineName, envVars):
    vagrantInstance = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    vagrantInstance.env = envVars
    vagrantInstance.destroy(vm_name=machineName)


@click.command()
@click.option("-e", "--envioronment", required=False, default="dev",
                    type=click.Choice(["dev", "prod", "stage"]))
@click.option("-a", "--action", required=False, default="up",
                    type=click.Choice(["up", "destroy"]))
def main(envioronment, action):
    if IsCertExist():
        SelfSignedCertificate()
    machineName = envioronment
    envVars = prepareEnvironmentVars(machineName)
    if (action == 'up'):
        startVagrant(machineName, envVars)
    elif (action == 'destroy'):
        destroyVagrant(machineName, envVars)


if __name__ == '__main__':
    main()
