# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'
AWS = YAML.load_file 'aws.yml'

Vagrant.configure("2") do |config|

    if Vagrant::Util::Platform.windows?
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

  config.vm.provision :shell, inline: "echo COMPOSE_PROJECT_NAME=devopsloft > /etc/profile.d/compose-project.sh", run: "always"

	config.vm.provision :ansible_local, run: 'always', type: :ansible_local do |ansible|
		ansible.compatibility_mode = "2.0"
		ansible.galaxy_role_file = 'playbooks/requirements.yml'
		ansible.galaxy_roles_path = '/vagrant/provisioning/playbooks/roles'
		ansible.galaxy_command = 'ansible-galaxy install --role-file=%{role_file} --roles-path=%{roles_path}'
		ansible.provisioning_path = '/vagrant/provisioning'
		ansible.inventory_path = 'hosts'
		ansible.playbook = 'playbooks/site.yml'
	end

	config.vm.define "dev" do |dev|

		dev.vm.box = "ubuntu/bionic64"
		dev.vm.network "forwarded_port", guest: 80, host: 5000

		config.vm.synced_folder ".", "/vagrant"

		dev.vm.provider :virtualbox do |virtualbox,override|
			virtualbox.name = "devopsloft_dev"
			virtualbox.memory = 1024
			virtualbox.cpus = 2
		end
	end

	config.vm.define "stage" do |stage|

		config.vm.synced_folder ".", "/vagrant",
														disabled: false,
														type: 'rsync',
														rsync__verbose: true,
														rsync__args: %w(
                              -a
                              --no-owner
															--no-group
                          	)

		stage.vm.box = "dummy"
		stage.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

		stage.vm.provider :aws do |aws,override|
			aws.keypair_name = AWS['stage_keypair_name']
			aws.ami = AWS['stage_ami']
			aws.instance_type = AWS['stage_instance_type']
			aws.region = AWS['stage_region']
			aws.subnet_id = AWS['stage_subnet_id']
			aws.security_groups = AWS['stage_security_groups']
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = AWS['stage_ssh_private_key_path']
		end

	end

	config.vm.define "prod" do |prod|

		config.vm.synced_folder ".", "/vagrant",
														disabled: false,
														type: 'rsync',
														rsync__verbose: true,
														rsync__args: %w(
                              -a
                              --no-owner
															--no-group
                          	)

		prod.vm.box = "dummy"
		prod.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

		prod.vm.provider :aws do |aws,override|
			aws.keypair_name = AWS['prod_keypair_name']
			aws.ami = AWS['prod_ami']
			aws.instance_type = AWS['prod_instance_type']
			aws.elastic_ip = AWS['prod_elastic_ip']
			aws.region = AWS['prod_region']
			aws.subnet_id = AWS['prod_subnet_id']
			aws.security_groups = AWS['prod_security_groups']
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = AWS['prod_ssh_private_key_path']
		end

	end
end
