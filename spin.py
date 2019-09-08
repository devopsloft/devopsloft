#!/usr/bin/env python3
import dotenv
import vagrant
import os
import click
from createPemFiles import SelfSignedCertificate, IsCertExist

vagrant_box = ""
vagrant_box_url = ""
vagrant_box_provider = ""
print_debug = 'No'


def print_info(message):
    if print_debug == 'yes':
        print("--- python debug ---> ", message)


def PrepareEnvironmentVars(environementName, action):
    # Reads the .env file from the repository
    # Returns an array with all the env vars, inclduing modificatoins per env
    global vagrant_box
    global vagrant_box_url
    global vagrant_box_provider

    dotenv.load_dotenv()
    envArray = os.environ.copy()
    envArray['RUN_BY_PYTHON'] = 'yes'

    if (environementName == 'dev'):
        envArray['WEB_HOST_PORT'] = envArray['DEV_WEB_HOST_PORT']
        envArray['WEB_GUEST_PORT'] = envArray['DEV_WEB_GUEST_PORT']
        envArray['WEB_HOST_SECURE_PORT'] = envArray['DEV_WEB_HOST_SECURE_PORT']
        envArray['WEB_GUEST_SECURE_PORT'] = \
            envArray['DEV_WEB_GUEST_SECURE_PORT']
        envArray['VAGRANT_RUN_COMMAND'] = action
        envArray['VAGRANT_ENV_COMMAND'] = environementName
        vagrant_box = envArray['DEV_VAGRANT_BOX']
        envArray['VAGRANT_BOX'] = envArray['DEV_VAGRANT_BOX']
        vagrant_box_url = envArray['DEV_VAGRANT_URL']
        envArray['VAGRANT_URL'] = vagrant_box_url
        vagrant_box_provider = envArray['DEV_VAGRANT_PROVIDER']
        envArray['VAGRANT_PROVIDER'] = vagrant_box_provider
    return envArray


def startVagrant(machineName, envVars):
    # Starts a Vagrant instance with noisy logs
    # Loading the enviornement vars that was created in prepareEnvironmentVars
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.env = envVars
#    v.up(vm_name=vagrant_box,provider=vagrant_box_provider)
    v.up()


def destroyVagrant(machineName, envArray):
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.env = envArray
    v.destroy(vm_name=machineName)


def updateBox(envArray):
    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
    v.env = envArray

    machines = v.box_list()
    for i in machines:
        print_info("Search machine: ")
        print_info(i)
        if i.name == vagrant_box:
            print_info("Found it: ")
            print_info(i)
            print_info("Update Machine: ")
            v.box_update()
            print_info("Prone Machine: ")
            v.box_prune()
            return
    print_info("Adding a new machine to your repository: ")
    print_info(vagrant_box)
    v.box_add(name=vagrant_box, url=vagrant_box_url,
              provider=vagrant_box_provider, force=True)
    v.box_update(vagrant_box, vagrant_box_provider)
    v.box_prune()\



@click.command()
@click.option("-e", "--envioronment", required=False, default="dev",
                    type=click.Choice(["dev", "prod", "stage"]))
@click.option("-a", "--action", required=False, default="up",
                    type=click.Choice(["up", "destroy"]))
@click.option("-d", "--debug", required=False, default="no",
                    type=click.Choice(["yes", "no"]))
def main(envioronment, action):
    machineName = envioronment
    envVars = (machineName)
    envVars = PrepareEnvironmentVars(envVars, action)

    if not (IsCertExist()):
        SelfSignedCertificate()

    if (action == 'up'):
        if (envioronment == 'dev'):
            updateBox(envVars)
        print("start Vagrant ...")
        startVagrant(machineName, envVars)
    elif (action == 'destroy'):
        destroyVagrant(machineName, envVars)


if __name__ == '__main__':
    main()
