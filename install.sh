#!/usr/bin/env bash


echo Adding snaptel repo for apt
curl -s https://packagecloud.io/install/repositories/intelsdi-x/snap/script.deb.sh | sudo bash
sudo apt-get install -y snap-telemetry

echo Installing pip
sudo apt-get update
sudo apt-get install -y python-pip

echo Installing python snaptel plugin lib
sudo pip install git+https://github.com/jcooklin/snap-plugin-lib-py

sudo service snap-telemetry start
export OS=$(uname -s | tr '[:upper:]' '[:lower:]')
export ARCH=$(uname -m)
curl -sfL "https://github.com/intelsdi-x/snap-plugin-publisher-file/releases/download/2/snap-plugin-publisher-file_${OS}_${ARCH}" -o snap-plugin-publisher-file
curl -sfL "https://github.com/intelsdi-x/snap-plugin-collector-psutil/releases/download/8/snap-plugin-collector-psutil_${OS}_${ARCH}" -o snap-plugin-collector-psutil
snaptel plugin load snap-plugin-publisher-file
snaptel plugin load snap-plugin-collector-psutil
curl https://raw.githubusercontent.com/intelsdi-x/snap/master/examples/tasks/psutil-file.yaml -o /tmp/psutil-file.yaml
snaptel task create -t /tmp/psutil-file.yaml
