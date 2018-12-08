#!/bin/bash

##############
# Prometheus #
##############

WORKING_DIR=/vagrant
cd $WORKING_DIR

# Create prometheus system user & group
sudo groupadd --system prometheus
sudo useradd -s /sbin/nologin -r -g prometheus prometheus

# Download
wget https://github.com/prometheus/prometheus/releases/download/v2.5.0/prometheus-2.5.0.linux-amd64.tar.gz

# Unpack
tar -zxvf prometheus-2.5.0.linux-amd64.tar.gz

cd $WORKING_DIR/prometheus-2.5.0.linux-amd64

# Create Data & Config dirs
sudo mkdir -p /etc/prometheus/{rules,rules.d,files_sd}  /var/lib/prometheus

# Add to $PATH
sudo cp prometheus promtool /usr/local/bin/
sudo cp -r consoles/ console_libraries/ /etc/prometheus/

# Copy Files
sudo cp /vagrant/monitoring_assets/prometheus.yml /etc/prometheus/
sudo cp /vagrant/monitoring_assets/os.rules /etc/prometheus/rules/
sudo cp /vagrant/monitoring_assets/prometheus.service /etc/systemd/system/prometheus.service

# Set permissions
sudo chown -R prometheus:prometheus /etc/prometheus/  /var/lib/prometheus/
sudo chmod -R 775 /etc/prometheus/ /var/lib/prometheus/

# # Start service & add to startup
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus

# # Delete package
cd $WORKING_DIR
rm -rf prometheus-*

#################
# Node Exporter #
#################

# Create unprivileged user
sudo useradd node_exporter -s /sbin/nologin

# Download
wget https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz
tar -zxvf node_exporter-0.17.0.linux-amd64.tar.gz

# adding to $PATH
sudo cp node_exporter-*.*-amd64/node_exporter /usr/sbin/


# Create node exporter config file, currently unused
sudo mkdir -p /etc/sysconfig
sudo touch /etc/sysconfig/node_exporter

# Copy Service
sudo cp /vagrant/monitoring_assets/node_exporter.service /etc/systemd/system/

# Enable & start service
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

# Remove unused files
rm -rf node_e*

#################
# Grafana #
#################
cd $WORKING_DIR

# Download
wget https://dl.grafana.com/oss/release/grafana_5.4.0_amd64.deb
sudo apt-get install -y adduser libfontconfig
sudo dpkg -i grafana_5.4.0_amd64.deb

# Delete unused files
rm -rf grafana*

# Place config files & dashbord
sudo cp -rf /vagrant/monitoring_assets/datasource.yml /etc/grafana/provisioning/datasources/
sudo cp -rf /vagrant/monitoring_assets/dashboard.yml /etc/grafana/provisioning/dashboards
sudo cp -rf /vagrant/monitoring_assets/DevopsLoft.json /etc/grafana/provisioning/dashboards/

# Start & Enable grafana service
sudo service grafana-server start
sudo update-rc.d grafana-server defaults
sudo systemctl enable grafana-server.service