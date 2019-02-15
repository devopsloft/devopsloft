# -*- mode: ruby -*-
# vi: set ft=ruby :

require './lib/vagrant.rb'
include OS

puts ""

if OS.windows?
    puts "Vagrant was launched from Windows."
elsif OS.mac?
    puts "Vagrant was launched from Mac."
elsif OS.unix?
    puts "Vagrant was launched from Unix."
elsif OS.linux?
    puts "Vagrant was launched from Linux."
else
    puts "Vagrant was launched from unknown platform."
end

Vagrant.configure("2") do |config|

    if OS.windows?
        # needed for windows as prerequisite for vagrant-aws but will work from vagrant next release 2.2.4
        if Vagrant::VERSION >= '2.2.4'
            required_plugins = [
            {"fog-ovirt" => {"version" => "1.0.1"}},
            "vagrant-aws"
            ]
            config.vagrant.plugins = required_plugins
        else
            unless Vagrant.has_plugin?("vagrant-aws")
                puts ""
                puts "Since you are using Windows with vagrant version " + Vagrant::VERSION + ","
                puts "You must install the following plugins manually:"
                puts "1. vagrant plugin install --plugin-version 1.0.1 fog-ovirt"
                puts "2. vagrant plugin install vagrant-aws"
                exit
            end
        end
    else
        required_plugins = [
            "vagrant-aws"
        ]
        config.vagrant.plugins = required_plugins
    end

	config.vm.synced_folder ".", "/vagrant", disabled: false, type: 'rsync'
	config.vm.provision :ansible_local do |ansible|
		ansible.playbook = "playbooks/bootstrap-infra.yml"
	end
	config.vm.provision "shell",path: "bootstrap-db.sh"
	config.vm.provision "shell",path: "bootstrap-app.sh"


	config.vm.define "dev" do |dev|

		dev.vm.box = "ubuntu/bionic64"
		dev.vm.network "forwarded_port", guest: 80, host: 5000

		dev.vm.provider :virtualbox do |virtualbox,override|
			virtualbox.name = "devopsloft_dev"
			virtualbox.memory = 1024
			virtualbox.cpus = 2
		end
	end

	config.vm.define "stage" do |stage|

		stage.vm.box = "dummy"
		stage.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

		stage.vm.provider :aws do |aws,override|
			aws.keypair_name = "osx_rsa"
			aws.ami = "ami-d2414e38"
			aws.instance_type = "t2.micro"
			aws.region = "eu-west-1"
			aws.subnet_id = "subnet-2c67fe64"
			aws.security_groups = ["sg-7b78fe07"]
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = "~/.ssh/osx_rsa.pem"
		end

	end

	config.vm.define "prod" do |prod|

		prod.vm.box = "dummy"
		prod.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"


		prod.vm.provider :aws do |aws,override|
			aws.keypair_name = "osx_rsa"
			aws.ami = "ami-d2414e38"
			aws.instance_type = "t2.micro"
			aws.elastic_ip = "52.209.230.146"
			aws.region = "eu-west-1"
			aws.subnet_id = "subnet-2c67fe64"
			aws.security_groups = ["sg-7b78fe07"]
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = "~/.ssh/osx_rsa.pem"
		end

	end
end
