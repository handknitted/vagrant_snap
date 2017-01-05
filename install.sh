#!/usr/bin/env bash

echo Adding snaptel repo for apt
curl -s https://packagecloud.io/install/repositories/intelsdi-x/snap/script.deb.sh | sudo bash
sudo apt-get install -y snap-telemetry

echo Installing pip
sudo apt-get update
sudo apt-get install -y python-pip

echo Installing python snaptel plugin lib
sudo pip install git+https://github.com/jcooklin/snap-plugin-lib-py

echo copying over my snaptel config file
sudo cp /vagrant_snap/files/snapteld.conf /etc/snap/.

sudo sudo sed -i "s/vagrant_snap\.tribe_bind_address/${BIND_IP}/g" /etc/snap/snapteld.conf
sudo sudo sed -i "s/vagrant_snap\.tribe_seed/$SEED_IP:6000/g" /etc/snap/snapteld.conf
sudo touch /etc/snap/snapd.conf
echo restarting snap-telemetry
sudo service snap-telemetry restart
# give the service a moment to collect itself - too quick and it complains that we haven't enabled tribe
sleep 1
echo Creating mmla agreement
snaptel agreement create mmla
snaptel agreement join mmla `hostname`
