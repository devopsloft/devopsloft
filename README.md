# <a href="http://www.devopsloft.io">DevOps Loft</a>

[![Build Status](https://travis-ci.org/devopsloft/devopsloft.svg?branch=master)](https://travis-ci.org/devopsloft/devopsloft)

<img src="http://www.devopsloft.io/static/logo.png" alt="drawing" width="250" hight="250"/>

#### Detailed prerequisites and instructions for spinning dev and stage environment


### DEV environment

<details>
  <summary>Prerequisites</summary>

  Install Docker (version 19.03.xx or higher)
  <ul>
    <li>
      <details>
        <summary>Windows 64bit or higher</summary>
        <p>Docker Desktop for Windows - <a href='https://docs.docker.com/docker-for-windows/install/'>link</a></p>
      </details>
    </li>
  <li><details>
    <summary>Windows 32bit or lower</summary>
    <p>Docker Toolbox for Windows - <a href='https://docs.docker.com/toolbox/toolbox_install_windows/'>link</a></P>
  </details></li>
  <li><details>
    <summary>Linux distros</summary>
				<ul>
					<li>Docker Engine - follow instructions by your distro <a href='https://docs.docker.com/engine/install/'>here</a></li>
					<li>Docker Compose - follow instructions by your distro <a href='https://docs.docker.com/compose/install/'>here</a></li>
				</ul>    
  </details></li>
  </ul>
</details>

<details>
  <summary>Spin DEV environment</summary>
  <ul>
  <li><details style="margin-left: 1em">
  <summary>Windows</summary>
  Execute the following commands <b>(run it from Git-Bash or similar and not from Command Prompt)</b>:
	
1. ```openssl req -x509 -newkey rsa:4096 -nodes -out web_s2i/cert.pem -keyout web_s2i/key.pem -days 365 -subj "/C=IL/ST=Gush-Dan/L=Tel-Aviv/O=DevOps Loft/OU=''/CN=''"``` **(this is one very long command line)**
2. Start docker on your machine (if it doesn't running already; way to start is based on your installation)
2. `docker build -t devopsloft/spinner .` **(don't forget the dot at the end)**
3. `docker-compose build`
4. `docker run --rm -d -v //var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest`
5. Browse: `http://localhost:5000/`
  </details></li>

  <li><details style="margin-left: 1em">
  <summary>Linux</summary>
  Execute the following commands:

1. ```openssl req -x509 -newkey rsa:4096 -nodes -out web_s2i/cert.pem -keyout web_s2i/key.pem -days 365 -subj "/C=IL/ST=Gush-Dan/L=Tel-Aviv/O=DevOps Loft/OU=''/CN=''"``` **(this is one very long command line)**
2. `docker build -t devopsloft/spinner .` **(don't forget the dot at the end)**
3. `docker-compose build`
4. `docker run --rm -d -v /var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest`
5. Browse: `http://localhost:5000/`
  </details></li>
  </ul>
</details>

<details>
  <summary>Teardown DEV environment</summary>
Execute the following commands:
<ul>
<li><details>
  <summary>Windows</summary>

1. `docker run --rm -d -v //var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest ./spin-docker.py --action destroy`
2. `docker image prune -af`
</details></li>

<li><details>
  <summary>Linux</summary>

1. `docker run --rm -d -v /var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest ./spin-docker.py --action destroy`
2. `docker image prune -af`
</details></li>
</ul>
</details>

---
### STAGE environment

<details>
  <summary>Prerequisites for Stage</summary>
  <ul>
    <li>Dockerhub account</li>
    <li>AWS account</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
    <li>keypair</li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li> AWS S3 Bucket</li>
  </ul>
</details>

<details>
  <summary>Spin STAGE environment</summary>

Execute the following:

1. `export NAMESPACE=<your dockerhub user>`
2. `docker build -t ${NAMESPACE}/spinner .`
3. `docker-compose build`
4. `docker-compose push`
5. `docker run --rm -d -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest -e stage`
6. Locate the EC2 instance Public DNS: AWS Consule->EC2->Insance->Public DNS (IPv4)
7. Browse <Public DNS>
</details>

<details>
<summary>Teardown STAGE environment</summary>

Execute the following:

1. `docker run --rm -d -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment stage --action destroy`
2. `docker image prune -af`

</details>