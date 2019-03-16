#!/usr/bin/env bash

# Update apt-get
apt-get update -y

# Update Ubuntu
apt-get -y upgrade
apt-get -y dist-upgrade

# Install recommended extra packages
apt-get install -y \
    linux-image-extra-$(uname -r) \
    linux-image-extra-virtual

# Allow apt to use repo over HTTPS
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Set up the stable repo
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Update the packages
apt-get update

# Install docker-ce
apt-get install -y docker-ce

# Access docker w/o sudo
usermod -aG docker vagrant
