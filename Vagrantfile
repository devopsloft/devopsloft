# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

	config.vm.define "dev" do |dev|

		dev.vm.box = "ubuntu/bionic64"
		dev.vm.provision "shell",path: "bootstrap-db.sh"
		dev.vm.provision "shell",path: "bootstrap-app.sh"
		dev.vm.network "forwarded_port", guest: 5000, host: 5000

		dev.vm.provider :virtualbox do |virtualbox,override|
			virtualbox.name = "devopsloft_dev"
			virtualbox.memory = 1024
			virtualbox.cpus = 2
		end
	end

	config.vm.define "stage" do |stage|

		stage.vm.synced_folder ".", "/vagrant", disabled: true
		stage.vm.box = "dummy"
		stage.vm.provision "file", source: ".", destination: "$HOME/devopsloft"
		stage.vm.provision "shell",path: "bootstrap-db.sh"
		stage.vm.provision "shell",path: "bootstrap-app.sh"
		stage.vm.network "forwarded_port", guest: 5000, host: 5000

		stage.vm.provider :aws do |aws,override|
			aws.keypair_name = "balex_IRL_rsa"
			aws.ami = "ami-d2414e38"
			aws.instance_type = "t2.micro"
			aws.region = "eu-west-1"
			aws.subnet_id = "subnet-d35c9789"
			aws.security_groups = ["sg-07780a80474a73bab"]
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = "C:\\Users\\balex\\.ssh\\balex_IRL_rsa.pem"
		end
	end

end
