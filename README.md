[![Build Status](https://travis-ci.org/devopsloft/devopsloft.svg?branch=master)](https://travis-ci.org/devopsloft/devopsloft)

# DevOps Loft

## Drive our Career Path into DevOps

A community which drives our career path into DevOps.

## Table of Contents

* [What does that mean?](#what-does-that-mean)
* [How?](#how)
* [Costs](#costs)
* [Weekly Sessions](#weekly-sessions)
* [Running the application](#running-the-application)

# What does that mean?

The community mission is transferring DevOps knowledge by practice. We are implementing an open source web app (www.devopsloft.io), while picking up DevOps technologies, like: git (GitHub), AWS, Linux, scripting, Jenkins, Chef/Ansible.

The goal of the community is addressing the lack of experienced DevOps specialists to fulfill the increasing demand.

# How?

Assisting you building a career path in the DevOps domain by driving DevOps knowledge transfer in a study group which develops a real webapp (www.devopsloft.io).
And, matching you with potentials organizations who seek DevOps engineers with your skillset (technical and personal).

We will study together DevOps, once a week, two hours session frontally using Skype or suchlike (shared lesson).
The rest of the work is done on your own. You will work on issues assigned to you.
One can order personal coaching/training.

You are welcomed to attend the program as long as you feel it is valuable for you.

According to your pace, we will set you interviews with potentials organizations.

Recommended skills:
A degree in Computer Science/Software Development/Industrial Engineering/related technical discipline or equivalent experience (DEV/IT/OPS)
Ability to understand and write code.

What to bring:
* yourself
* your laptop

We will be working with services like: GitHub, AWS and others. Some of those services require payments. Those costs are on your own expense.

# Costs

Participation is free of charge and commitment

# Weekly Sessions
(online or offline)

Every Wednesday 6:00pm-9:00pm IDT
</br>
</br>
If you'd like to add a feature or correct a defect, please open a
[pull request](https://github.com/DevOpsLoft/DevOpsLoft/pulls).</br>
If you have questions or suggestions, please open an
[issue](https://github.com/DevOpsLoft/DevOpsLoft/issues).

And be sure to follow us on [Facebook](https://facebook.com/devopsloft) and [LinkedIn](https://www.linkedin.com/company/devopsloft).

And ... join our [Facebook Group](https://www.facebook.com/groups/512664539127088) and our [Meetup Group](https://www.meetup.com/DevOps-Tel-Aviv/).

# Running the application

## Prerequisites

* Vagrant should be installed in order to launch an environment of the application.
* AWS account is required in order to run the application in STAGE environment. (see more details in STAGE Environment section)

### Docker secrets and configurations
The following settings are advised to be set in `.env` file:
* MYSQL_ROOT_PASSWORD - Default: root
* MYSQL_EXPORTER_PASSWORD - Default: exporter
* MYSQL_APPLICATION_PASSWORD - Default: application

## DEV environment

* The application will be deployed via docker-compose
* Create the environment

```
docker-compose up -d
```

* Access the application through internet browser
```
localhost:5000
```

If a change is made to a container, it needs to be rebuilt.
Use the following: (`python-app` is just an example here)
```
docker-compose build python-app
docker-compose up -d --force-recreate python-app
```

### MySQL data
in the folder `database` we can add `.sql` and `.sh` files that will be executed upon MySQL
container startsup.

**important**
* The commands must be idempotent
* The commands only run once if the DB files are not present, this is not a migration tool, it's a seeding tool
* Until there is a DB migrations tool, for clarity, changes should be set in a manner that follow "migrations" patterns, for example:
Adding a column to an existing table:
```sql
CREATE TABLE IF NOT EXISTS devopsloft.users
(id integer NOT NULL AUTO_INCREMENT, 
 first_name varchar(100) NOT NULL)
ALTER TABLE devopsloft.users ADD example integer;
```
Creating a user:
```sql
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
ALTER USER 'user'@'%' IDENTIFIED BY 'password';
```
Preferably, place the creation of the user in `.sh` to be able to access environment variables.
The files are processed in lexicographic order

##### Purging all MySQL data #####
```bash
docker-compose stop mysql
docker-compose rm -f mysql
docker volumde rm devopsloft_mysql-data
```
Then you will need to start up the container again
```bash
docker-compose up -d mysql
```

## STAGE environment

!!! Don't share your private Access Key and don't push it to GitHub

* AWS account with the following configurations
  * Keypair (deployed on your computer)
  * AMI ID
  * Subnet ID
  * Security Group with inbound ports for SSH and TCP port 5000
* Adjust `Vagrantfile.local` with your configuration (see the Vagrantfile.local.example file for reference)
* Install Vagrant AWS plugin
```
vagrant plugin install vagrant-aws
```
* Launch the environment
```
vagrant up stage
```
* Access the application using Public DNS/IP of the created instance + port 5000
* !!! Don't forget to destroy the instance when you done to avoid unnecessary charges
```
vagrant destroy --force stage
```
