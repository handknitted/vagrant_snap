#!/usr/bin/env bash

sudo apt-get -y install graphite-web apache2 libapache2-mod-wsgi

sudo DEBIAN_FRONTEND=noninteractive apt-get -q -y --force-yes install graphite-carbon

sudo -H -u _graphite bash -c 'echo no | graphite-manage syncdb'

sudo a2dissite 000-default
sudo cp /usr/share/graphite-web/apache2-graphite.conf /etc/apache2/sites-available
sudo a2ensite apache2-graphite
sudo service apache2 reload

