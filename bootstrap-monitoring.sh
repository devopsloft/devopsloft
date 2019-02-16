#!/usr/bin/env bash

##############
# Prometheus #
##############

WORKING_DIR=/vagrant
cd $WORKING_DIR

# Create prometheus system user & group
groupadd --system prometheus
useradd -s /sbin/nologin -r -g prometheus prometheus

# Download
wget https://github.com/prometheus/prometheus/releases/download/v2.5.0/prometheus-2.5.0.linux-amd64.tar.gz

# Unpack
tar -zxvf prometheus-2.5.0.linux-amd64.tar.gz

cd $WORKING_DIR/prometheus-2.5.0.linux-amd64

# Create Data & Config dirs
mkdir -p /etc/prometheus/{rules,rules.d,files_sd} /var/lib/prometheus /etc/prometheus/rules/

# Add to $PATH
cp prometheus promtool /usr/local/bin/
cp -r consoles/ console_libraries/ /etc/prometheus/

# Copy Files
cp /vagrant/monitoring_assets/prometheus.yml /etc/prometheus/
cp /vagrant/monitoring_assets/os.rules /etc/prometheus/rules/
cp /vagrant/monitoring_assets/prometheus.service /etc/systemd/system/prometheus.service

# Set permissions
chown -R prometheus:prometheus /etc/prometheus/  /var/lib/prometheus/
chmod -R 775 /etc/prometheus/ /var/lib/prometheus/

# # Start service & add to startup
systemctl daemon-reload
systemctl start prometheus
systemctl enable prometheus

# # Delete package
cd $WORKING_DIR
rm -rf prometheus-*

#################
# Node Exporter #
#################

# Create unprivileged user
useradd node_exporter -s /sbin/nologin

# Download
wget https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz
tar -zxvf node_exporter-0.17.0.linux-amd64.tar.gz

# adding to $PATH
cp node_exporter-*.*-amd64/node_exporter /usr/sbin/


# Create node exporter config file, currently unused
mkdir -p /etc/sysconfig
touch /etc/sysconfig/node_exporter

# Copy Service
cp /vagrant/monitoring_assets/node_exporter.service /etc/systemd/system/

# Enable & start service
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter

# Remove unused files
rm -rf node_e*

#################
# Grafana #
#################
cd $WORKING_DIR

# Download
wget https://dl.grafana.com/oss/release/grafana_5.4.0_amd64.deb
apt-get install -y adduser libfontconfig
dpkg -i grafana_5.4.0_amd64.deb

# Delete unused files
rm -rf grafana*

# Place config files & dashbord
cp -rf /vagrant/monitoring_assets/datasource.yml /etc/grafana/provisioning/datasources/
cp -rf /vagrant/monitoring_assets/dashboard.yml /etc/grafana/provisioning/dashboards
cp -rf /vagrant/monitoring_assets/devopsloft.json /etc/grafana/provisioning/dashboards/

# Start & Enable grafana service
service grafana-server start
update-rc.d grafana-server defaults
systemctl enable grafana-server.service
