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

 1. In the root directory of the project run `docker build -t spinner .`
 2. Run `docker run -t -d --name spincontainer -v /var/run/docker.sock:/var/run/docker.sock spinner`
 3. Run `docker exec -it spincontainer bash`
 4. Run `python spin-docker.py`
 
##### Cleanup Environment

Run the following to cleanup your environment

1. docker exec -it spincontainer bash
2. python spin-docker.py --action destroy
3. docker rm -f spincontainer
4. docker rmi spinner
