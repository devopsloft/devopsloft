# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell",path: "bootstrap.sh"
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provider "virtualbox" do|v|
	v.name = "devopsloft_dev"
	v.memory = 1024
	v.cpus = 2
  end
end
