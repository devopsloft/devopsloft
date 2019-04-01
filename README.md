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
* devopsloft.yml file - feature toggle. Feature is released if the value is 'enabled'. 

## DEV environment

* The application will be deployed as local VM using VirtualBox
* Create the environment

```
vagrant up dev
```

* Access the application through internet browser
```
localhost:5000
```

## STAGE environment

!!! Don't share your private Access Key and don't push it to GitHub

* AWS account with the following configurations
  * Keypair (deployed on your computer)
  * AMI ID
  * Subnet ID
  * Security Group with inbound ports for SSH and TCP port 5000
* Copy the file `aws.yml` to `aws.yml.local`
* Adjust `aws.yml.local` with **your** configuration
* Vagrant AWS plugin or any dependencies are done automatic on the **first run**
* Launch the environment
```
vagrant up stage
```
* Access the application using Public DNS/IP of the created instance + port 5000
* !!! Don't forget to destroy the instance when you done to avoid unnecessary charges
```
vagrant destroy --force stage
```
