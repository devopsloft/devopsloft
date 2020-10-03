# <a href="http://www.devopsloft.io">DevOps Loft</a>

[![ci](https://github.com/devopsloft/devopsloft/workflows/ci/badge.svg)](https://github.com/devopsloft/devopsloft/actions?query=workflow%3Aci)

<img src="http://www.devopsloft.io/logo.png" alt="drawing" width="250" hight="250"/>

#### Detailed prerequisites and instructions for spinning DEV/STAGE/PROD environments

### DEV environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Install Docker (version 19.03.xx or higher)</li>
    <li>Install Docker Compose (version 1.25.5 or higher)</li>
    <li>AWS account</li>
    <li>AWS Profile</li>
    <li>Create an envfile '.env.dev' from the example '.env.dev.example'</li>
    <li>Chrome - Allows requests to localhost over HTTPS even when an invalid certificate is presented. `chrome://flags/#allow-insecure-localhost`</li>
  </ul>
</details>

<details>
  <summary>Spin DEV environment</summary>
  Execute the following commands:

1. `./build/build.sh dev`
2. `source .env.dev`
3. `docker run --rm -v $HOME/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest` 
4. Browse: `https://localhost:8443`

</details>

<details>
  <summary>Teardown DEV environment</summary>
Execute the following commands:

1. `./build/build.sh dev`
2. `source .env.dev`
3. `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --action destroy` 
4. `docker image prune -af`
5. `docker volume prune -f`

</details>

---

### STAGE environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Dockerhub account</li>
    <li>AWS account</li>
    <li>AWS Profile</li>
    <li>Terraform</li>
    <li>Docker</li>
    <li>Docker Compose</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li>AWS S3 Bucket</li>
    <li>Create an envfile '.env.stage' from the example '.env.stage.example'</li>
  </ul>
</details>

<details>
  <summary>Spin STAGE environment</summary>

Execute the following:

1. `./build/build.sh stage`
2. `source .env.stage`
3. `terraform init deply`
4. `terraform apply --var-file=deploy/aws-stage.tfvars deploy`
5. `docker run --rm -v $HOME/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT` 
6. Locate the EC2 instance Public DNS: AWS Consule->EC2->Insance->Public DNS (IPv4)
7.  Browse <Public DNS>

</details>

<details>
<summary>Teardown STAGE environment</summary>

Execute the following:

1. `./build/build.sh stage`
2. `docker run --rm -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT --action destroy` 
3. `docker image prune -af` 

</details>

---

### PROD environment

<details>
  <summary>Prerequisites</summary>
  <ul>
    <li>Dockerhub account</li>
    <li>AWS account</li>
    <li>AWS Profile</li>
    <li><a href='https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html'>AWS ~/.aws or %UserProfile%\.aws folder</a></li>
    <li>keypair</li>
    <li>subnet ID</li>
    <li>Security Group with inbound ports for SSH (22), HTTP (80), HTTPS (443), and 8200</li>
    <li>AWS S3 Bucket</li>
    <li>Elastic IP Address (EIP)</li>
    <li>Create an envfile '.env.prod' from the example '.env.prod.example'</li>
  </ul>
</details>

<details>
<summary>Teardown PROD environment</summary>

Execute the following:

1. `./build/build.sh prod`
2. `source .env.prod`
3. `terraform init deply`
4. `terraform apply --var-file=deploy/aws-prod.tfvars deploy`
5. `docker run --rm -v ~/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT --action destroy` 
6. `docker image prune -af` 

</details>

<details>
  <summary>Spin PROD environment</summary>

Execute the following:

1. `./build/build.sh prod`
6. `docker run --rm -v $HOME/.aws:/root/.aws -v /var/run/docker.sock:/var/run/docker.sock ${NAMESPACE}/spinner:latest ./spin-docker.py --environment $ENVIRONMENT` 
7.  Browse www.devopsloft.io

</details>

