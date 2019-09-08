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

##### Spin environment

~~~
  ./spin.py up [dev|stage]
~~~

##### SSH the environment

~~~
  vagrant ssh [dev|stage]
~~~

##### !!! Don't forget to destroy the environment when you done to avoid unnecessary charges

~~~
  ./spin.py destroy [dev|stage]
~~~

#### Notes

-   Do not use vagrant directly to spin and environment. It might work, but most likely it won't
