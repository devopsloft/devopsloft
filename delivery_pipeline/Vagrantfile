Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "forwarded_port",
    guest: 4444,
    host: 4444

  config.vm.provision :docker
  config.vm.provision :docker_compose,
    compose_version: "1.24.0",
    yml: "/vagrant/docker-compose.yml",
    run: "always"

end
