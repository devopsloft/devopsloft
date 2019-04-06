# -*- mode: ruby -*-
# vi: set ft=ruby :

# -------------------------------------------------------------
# Exit if no environment name specified.
# -------------------------------------------------------------

$script = <<-SCRIPT
docker cp /vagrant/.secrets.json web:/.secrets.json
docker exec web ./events.py
SCRIPT

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
    if not (environments.include?ARGV[1] or environments.include?ARGV[2])
      puts "You must use 'vagrant #{ARGV[0]} " + environments.join("/") + "....'"
      puts "Run 'vagrant status' to view VM names."
      exit 1
    end
end

if ARGV[1] == 'dev' || ARGV[2] == 'dev'
  chosen_environment = 'dev'
elsif ARGV[1] == 'stage' || ARGV[2] == 'stage'
  chosen_environment = 'stage'
elsif ARGV[1] == 'prod' || ARGV[2] == 'prod'
  chosen_environment = 'prod'
end

$set_environment_variables = <<SCRIPT
tee -a "/vagrant/.env" >> "/dev/null" <<EOF
ENVIRONMENT=#{chosen_environment}
EOF
cp /vagrant/.env /vagrant/web_s2i/
cp /vagrant/.env /vagrant/db_s2i/
SCRIPT

puts 'Working on environment: ' + chosen_environment if chosen_environment

require 'yaml'
Vagrant.require_version ">= 2.2.4"

if chosen_environment != 'dev' # aws plugin is needed only for non dev environment
    if Vagrant::Util::Platform.windows?
        # needed for windows as prerequisite for vagrant-aws
        required_plugins = [
        {"fog-ovirt" => {"version" => "1.0.1"}},
        "vagrant-aws",
        ]
    else
        required_plugins = [
            "vagrant-aws",
        ]
    end
end

required_plugins = %w(vagrant-env)

plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
if not plugins_to_install.empty?
  puts "Installing plugins: #{plugins_to_install.join(' ')}"
  if system "vagrant plugin install #{plugins_to_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort "Installation of one or more plugins has failed. Aborting."
  end
end

Vagrant.configure("2") do |config|
    config.vagrant.plugins = required_plugins

    if File.exist?('.env.local')
        Dotenv.load('.env.local')
    end

    config.vm.provision 'shell',
    inline: $set_environment_variables, run: "always"

    config.env.enable
    config.vm.synced_folder '.', ENV['BASE_FOLDER'], disabled: false, type: 'rsync'

  config.vm.provision "docker" do |d|
    d.post_install_provision "shell", inline:"docker network create devopsloft_network"
    d.build_image ENV['BASE_FOLDER'] + '/db_s2i',
      args: '-t ' + ENV['NAMESPACE'] + '/' + ENV['DOCKERHUB_DB'] + ' --build-arg MYSQL_DATABASE=' + ENV['MYSQL_DB']
    d.run "db",
      image: ENV['NAMESPACE'] + '/' + ENV['DOCKERHUB_DB'],
      args: '--network devopsloft_network -p ' + ENV['MYSQL_PORT'] +':' + ENV['MYSQL_PORT'] + ' -e MYSQL_ROOT_PASSWORD=' + ENV['MYSQL_ROOT_PASSWORD'] + ' -e MYSQL_DATABASE=' + ENV['MYSQL_DB']
    d.build_image ENV['BASE_FOLDER'] + '/web_s2i',
      args: '-t ' + ENV['NAMESPACE'] + '/' + ENV['APP']
    d.run "web",
      image: ENV['NAMESPACE'] + '/' + ENV['APP'],
      args: '--network devopsloft_network -p ' + ENV['APP_GUEST_PORT'] +':' + ENV['APP_GUEST_PORT']
  end

  DEVOPSLOFT = YAML.load_file 'devopsloft.yml'
  if DEVOPSLOFT['publish'] == 'enabled'
    config.vm.provision "shell", inline: $script
  end

	config.vm.define "dev" do |dev|

		dev.vm.box = "ubuntu/bionic64"
		dev.vm.network "forwarded_port", guest: ENV['APP_GUEST_PORT'], host: ENV['APP_HOST_PORT']

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
			aws.keypair_name = ENV['STAGE_KEYPAIR_NAME']
			aws.ami = ENV['STAGE_AMI']
			aws.instance_type = ENV['STAGE_INSTANCE_TYPE']
			aws.region = ENV['STAGE_REGION']
			aws.subnet_id = ENV['STAGE_SUBNET_ID']
			aws.security_groups = ENV['STAGE_SECURITY_GROUPS']
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = ENV['STAGE_SSH_PRIVATE_KEY_PATH']
		end

	end

	config.vm.define "prod" do |prod|

		prod.vm.box = "dummy"
		prod.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"


		prod.vm.provider :aws do |aws,override|
			aws.keypair_name = ENV['PROD_KEYPAIR_NAME']
			aws.ami = ENV['PROD_AMI']
			aws.instance_type = ENV['PROD_INSTANCE_TYPE']
			aws.elastic_ip = ENV['PROD_ELASTIC_IP']
			aws.region = ENV['PROD_REGION']
			aws.subnet_id = ENV['PROD_SUBNET_ID']
			aws.security_groups = ENV['PROD_SECURITY_GROUPS']
			aws.associate_public_ip = true

			override.ssh.username = "ubuntu"
			override.ssh.private_key_path = ENV['PROD_SSH_PRIVATE_KEY_PATH']
		end

	end
end
