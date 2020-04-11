# <a href="http://www.devopsloft.io">DevOps Loft</a>

[![Build Status](https://travis-ci.org/devopsloft/devopsloft.svg?branch=master)](https://travis-ci.org/devopsloft/devopsloft)

<img src="http://www.devopsloft.io/static/logo.png" alt="drawing" width="250" hight="250"/>

### Spinning [dev|stage] environment

<details>
  <summary>Global Prerequisites</summary>
  <ul>
    <li>python 3</li>
    <li>Use `.env.local` file for configuration keys which overrides `.env`</li>
  </ul>
</details>

#### DEV environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Verify /vault directory exists and is writable</li>
    <li>For Windoes 10 Home users</li>
      <ul>
        <li>Docker toolbox</li>
        <li>docker-cli (`choco install docker-cli` - using prompt)</li>
        <li>docker-compose (`choco install docker-compose` - using prompt)</li>
      </ul>
  </ul>
</details>

#### STAGE environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>AWS account</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
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

##### Run the app on Windows 10 Home

1. Run `docker-machine env default`
2. Run `eval $(docker-machine env default --shell linux)`
3. In the root directory of the project run `docker build -t spinner .`
4. Run `docker run -t -d --name spincontainer -v %UserProfile%\.aws:/root/.aws -v //var/run/docker.sock:/var/run/docker.sock spinner`
5. Run `winpty docker exec -it spincontainer bash`
6. Run `python spin-docker.py`
7. Check the ip for your lochalhost - on the host machine run `docker-machine ip default`

##### Spin DEV environment

Execute the following:

`docker run --entrypoint ./spin-docker.py -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest`

##### Teardown DEV environment

Execute the following:

1. `docker run -td --name spinner -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest`
2. `docker exec -it spinner bash`
3. `./spin-docker.py --action destroy`
4. `exit`
5. `docker rm -f spinner`
6. `docker rmi devopsloft/spinner`
   

