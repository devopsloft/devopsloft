#!/usr/bin/env python3
import platform
import dotenv
import vagrant
import sys
import os


def findPlatformName():
    platformType = platform.system()
    return platformType


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


try:
    inputEnvironmentName = sys.argv[1]  # Should be: dev,prod or stage
except IndexError:
    print('You should enter the environement name you want to start')
    raise
envVar = prepareEnvironmentVars(inputEnvironmentName)
startVagrant(inputEnvironmentName, envVar)
