# <a href="http://www.devopsloft.io">DevOps Loft</a>

[![Build Status](https://travis-ci.org/devopsloft/devopsloft.svg?branch=master)](https://travis-ci.org/devopsloft/devopsloft)

<img src="http://www.devopsloft.io/static/logo.png" alt="drawing" width="250" hight="250"/>

## Contributing

### Spinning [dev|stage] environment

<details>
  <summary>Global Prerequisites</summary>
  <ul>
    <li>python 3</li>
    <li>vagrant</li>
    <li>vagrant plugin: vagrant-env</li>
    <li>Use `.env.local` file for configuration keys which overrides `.env`</li>
  </ul>
</details>

#### DEV environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>VirtualBox</li>
    <li>Verify /vault directory exists and is writable</li>
        <li>Install the following packages: </li>
          <li>virtualbox</li>
        <li>fabric3</li>
        <li>docker-compose</li>
 
  </ul>
</details>

#### STAGE environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>AWS account</li>
    <li>AWS credentials: access key & access secret</li>
    <li>keypair</li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li> AWS S3 Bucket</li>
  </ul>
</details>

##### Installation Requirements

On Linux, run the following commands

```
python -m venv ~/devopsloft_venv
source ~/devopsloft_venv/bin/active
pip install -r requirements.txt
```

Also make sure you have Docker installed on the system where you plan to run the application.

##### Run the app

1.  In the root directory of the project run `docker build -t spinner .`
2.  Run `docker run -t -d --name spincontainer -v /var/run/docker.sock:/var/run/docker.sock spinner`
3.  Run `docker exec -it spincontainer bash`
4.  Run `python spin-docker.py`

##### Cleanup Environment

Run the following to cleanup your environment

1. docker exec -it spincontainer bash
2. python spin-docker.py --action destroy
3. docker rm -f spincontainer
4. docker rmi spinner

##### Run the app on Windows 10 Home

<details>
  <summary>Windowws 10 Home Prerequisites</summary>
  <ul>
    <li>Docker toolbox</li>
    <li>docker-cli (`choco install docker-cli` - using prompt)</li>
    <li>docker-compose (`choco install docker-compose` - using prompt)</li>
  </ul>
</details>

We need to set up our Docker environment variables. This is to allow the Docker client and Docker Compose to communicate with the Docker Engine running in the Linux VM, `default`. You can do this by executing the commands in Git Bash:

```
# Print out docker machine instance settings
$ docker-machine env default

# Set environment variables using Linux 'export' command
$ eval $(docker-machine env default --shell linux)
```

You’ll need to set the environment variables every time you start a new Git Bash terminal. If you’d like to avoid this, you can copy `eval` output and save it in your `.bashrc` file. It should look something like this:

```
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.101:2376"
export DOCKER_CERT_PATH="C:\Users\Michael Wanyoike\.docker\machine\machines\default"
export DOCKER_MACHINE_NAME="default"
export COMPOSE_CONVERT_WINDOWS_PATHS="true"
```

<strong>IMPORTANT</strong> for the `DOCKER_CERT_PATH`, you’ll need to change the Linux file path to a Windows path format. Also take note that there’s a chance the IP address assigned might be different from the one you saved every time you start the `default` VM.

1. In the root directory of the project run `docker build -t spinner .`
2. Run `docker run -t -d --name spincontainer -v //var/run/docker.sock:/var/run/docker.sock spinner`
3. Run `winpty docker exec -it spincontainer bash`
4. Run `python spin-docker.py`

To cheack the ip for the lochalhost you need to return to the host and run `docker-machine ip default`. We are using port 5000.
