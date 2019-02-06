# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

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
