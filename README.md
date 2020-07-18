# <a href="http://www.devopsloft.io">DevOps Loft</a>

[![ci](https://github.com/devopsloft/devopsloft/workflows/ci/badge.svg)](https://github.com/devopsloft/devopsloft/actions?query=workflow%3Aci)

<img src="http://www.devopsloft.io/logo.png" alt="drawing" width="250" hight="250"/>

#### Detailed prerequisites and instructions for spinning DEV/STAGE/PROD environments

### DEV environment

<details>
  <summary>Prerequisites</summary>
    Install Docker (version 19.03.xx or higher)</br>
    Install Docker Compose (version 1.25.5 or higher)
    <ul>
    <li>
      <details>
        <summary>Windows 64bit or higher</summary>
        <p>Docker Desktop for Windows - <a href='https://docs.docker.com/docker-for-windows/install/'>link</a></p>
      </details>
    </li>
    <li>
      <details>
        <summary>Windows 32bit or lower</summary>
        <p>Docker Toolbox for Windows - <a href='https://docs.docker.com/toolbox/toolbox_install_windows/'>link</a></P>
      </details>
    </li>
    <li>
      <details>
        <summary>Linux distros</summary>
        <ul>
          <li>Docker Engine - follow instructions by your distro <a href='https://docs.docker.com/engine/install/'>here</a></li>
          <li>Docker Compose - follow instructions by your distro <a href='https://docs.docker.com/compose/install/'>here</a></li>
        </ul>    
      </details>
    </li>
    </ul>
    Create an envfile '.env.dev' from the template '.env.dev.template'
</details>

<details>
  <summary>Spin DEV environment</summary>
  <ul>
  <li><details style="margin-left: 1em">
  <summary>Windows</summary>
  Execute the following commands <b>(run it from Git-Bash or similar and not from Command Prompt)</b>:

	

1. `openssl req -x509 -newkey rsa:4096 -nodes -out web_s2i/cert.pem -keyout web_s2i/key.pem -days 365 -subj "/C=IL/ST=Gush-Dan/L=Tel-Aviv/O=DevOps Loft/OU=''/CN=''"` **(this is one very long command line)**
2. Start docker on your machine (if it doesn't running already; way to start is based on your installation)
3. `docker build -t devopsloft/spinner .` **(don't forget the dot at the end)**
4. `docker-compose build` 
5. `docker run --rm -d -v //var/run/docker.sock:/var/run/docker.sock devopsloft/spinner:latest` 
6. Browse: `http://localhost:5000/` 

  </details></li>

  <li><details style="margin-left: 1em">
  <summary>Linux</summary>
  Execute the following commands:

1. `source .env.dev` 
2. `openssl req -x509 -newkey rsa:4096 -nodes -out web_s2i/cert.pem -keyout web_s2i/key.pem -days 365 -subj "/C=IL/ST=Gush-Dan/L=Tel-Aviv/O=DevOps Loft/OU=''/CN=''"` 
3. `docker build --build-arg ENVIRONMENT=$ENVIRONMENT -t ${NAMESPACE}/spinner .` 
4. `docker-compose --env-file .env.$ENVIRONMENT build` 
5. `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest` 
6. Browse: `http://localhost:5000/` 

  </details></li>
  </ul>
</details>

<details>
  <summary>Teardown DEV environment</summary>
Execute the following commands:
<ul>
<li><details>
  <summary>Windows</summary>

1. `docker run --rm -d -v //var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --action destroy` 
2. `docker image prune -af` 

</details></li>

<li><details>
  <summary>Linux</summary>

1. `docker run --rm -d -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --action destroy` 
2. `docker image prune -af` 

</details></li>
</ul>
</details>

---

### STAGE environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Dockerhub account</li>
    <li>AWS account</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
    <li>keypair</li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li>AWS S3 Bucket</li>
    <li>Create an envfile '.env.stage' from the template '.env.stage.template'</li>
  </ul>
</details>

<details>
  <summary>Spin STAGE environment</summary>

Execute the following:

1. `source .env.stage` 
2. `docker build --build-arg ENVIRONMENT=$ENVIRONMENT -t ${NAMESPACE}/spinner .` 
3. `docker-compose --env-file .env.$ENVIRONMENT build` 
4. `docker-compose --env-file .env.$ENVIRONMENT push` 
5. `docker run --rm -v $HOME/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT` 
6. Locate the EC2 instance Public DNS: AWS Consule->EC2->Insance->Public DNS (IPv4)
7.  Browse <Public DNS>

</details>

<details>
<summary>Teardown STAGE environment</summary>

Execute the following:

1. `docker run --rm -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT --action destroy` 
2. `docker image prune -af` 

</details>

---

### PROD environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Dockerhub account</li>
    <li>AWS account</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
    <li>keypair</li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li>AWS S3 Bucket</li>
    <li>Elastic IP Address (EIP)</li>
    <li>Create an envfile '.env.prod' from the template '.env.prod.template'</li>
  </ul>
</details>

<details>
  <summary>Spin PROD environment</summary>

Execute the following:

1. `source .env.prod` 
2. `docker build --build-arg ENVIRONMENT=$ENVIRONMENT -t ${NAMESPACE}/spinner .` 
3. `docker-compose --env-file .env.$ENVIRONMENT build` 
4. `docker-compose --env-file .env.$ENVIRONMENT push` 
5. `docker run --rm -v $HOME/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT` 
6.  Browse www.devopsloft.io

</details>

<details>
<summary>Teardown PROD environment</summary>

Execute the following:

1. `docker run --rm -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT --action destroy` 
2. `docker image prune -af` 

</details>
