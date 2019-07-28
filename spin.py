#!/usr/bin/env python3

from checkPythonVer import checkPythonMinVer
checkPythonMinVer(3,6)

try:
    import dotenv
    import vagrant
    import os
    import click
    from createPemFiles import SelfSignedCertificate, IsCertExist
except ImportError:
    with open("./requirements.txt", 'r') as fin:
        print ("Make sure the following imports were done before running this program:")
        print ("*********")
        print (fin.read())
        print ("*********:")


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
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.env = envVars
    v.up(vm_name=machineName)


def destroyVagrant(machineName, envVars):
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.env = envVars
    v.destroy(vm_name=machineName)


def updateBox():
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.box_update()
    v.box_prune()


@click.command()
@click.option("-e", "--envioronment", required=False, default="dev",
                    type=click.Choice(["dev", "prod", "stage"]))
@click.option("-a", "--action", required=False, default="up",
                    type=click.Choice(["up", "destroy"]))
def main(envioronment, action):
    if not (IsCertExist()):
        SelfSignedCertificate()
    machineName = envioronment
    envVars = prepareEnvironmentVars(machineName)
    if (action == 'up'):
        if (envioronment == 'dev'):
            updateBox()
        startVagrant(machineName, envVars)
    elif (action == 'destroy'):
        destroyVagrant(machineName, envVars)


if __name__ == '__main__':
    main()
