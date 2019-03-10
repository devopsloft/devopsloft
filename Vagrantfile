# -*- mode: ruby -*-
# vi: set ft=ruby :

# -------------------------------------------------------------
# Exit if no environment name specified.
# -------------------------------------------------------------

environments = [
    "dev",
    "stage",
    "prod"
]
commandsToCheck = [
    "destroy",
    "halt",
    "provision",
    "reload",
    "resume",
    "suspend",
    "up"
  ]
  enteredCommand = ARGV[0]

  # Is this one of the problem commands?
  if commandsToCheck.include?(enteredCommand)
    # Is this command lacking any other supported environments ? e.g. "vagrant destroy dev".
    if not environments.include?ARGV[1]
      puts "You must use 'vagrant #{ARGV[0]} " + environments.join("/") + "....'"
      puts "Run 'vagrant status' to view VM names."
      exit 1
    end
  end

require 'yaml'
AWS = YAML.load_file 'aws.yml'

if File.exist?('aws.yml.local')
    private_settings = YAML::load_file('aws.yml.local')
    AWS.merge!(private_settings)
end

Vagrant.require_version ">= 2.2.4"

Vagrant.configure("2") do |config|

    if ARGV[1] != 'dev' # aws plugin is needed only for non dev environment
        if Vagrant::Util::Platform.windows?
            # needed for windows as prerequisite for vagrant-aws
            required_plugins = [
            {"fog-ovirt" => {"version" => "1.0.1"}},
            "vagrant-aws"
            ]
        else
            required_plugins = [
                "vagrant-aws"
            ]
        end
        config.vagrant.plugins = required_plugins
    end

	config.vm.synced_folder ".", "/vagrant", disabled: false, type: 'rsync'

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
