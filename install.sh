#!/bin/bash
set -e
source /pd_build/buildconfig

header "Installing python..."
run apt update
run apt install -y python python-pip
run pip install requests prometheus_client

header "Performing miscellaneous preparation"

## Create a user to run as the app.
run addgroup --gid 9999 app
run adduser --uid 9999 --gid 9999 --disabled-password --gecos "user to run the app" app
run usermod -L app


header "Installing beeping..."
## Install beeping.
run mkdir /etc/service/beeping
run mkdir -p /opt/GeoIP
run cp /pd_build/runit/beeping /etc/service/beeping/run
run cp /pd_build/files/beeping /usr/local/bin/
run cp /pd_build/files/GeoLite2-City.mmdb /opt/GeoIP/

header "Installing beeping_exporter..."
## Install beeping_exporter.
run mkdir /etc/service/beeping_exporter
run cp /pd_build/runit/beeping_exporter /etc/service/beeping_exporter/run
run cp /pd_build/files/beeping_exporter.py /usr/local/bin/



header "Finalizing..."

# disable services
run touch /etc/service/syslog-forwarder/down
run touch /etc/service/syslog-ng/down
run touch /etc/service/sshd/down

run apt-get remove -y autoconf automake
run apt-get autoremove
run apt-get clean
run rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
run rm -rf /pd_build
