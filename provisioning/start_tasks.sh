#!/usr/bin/env bash
echo Setting up plugins and tasks for mmla agreement
export OS=$(uname -s | tr '[:upper:]' '[:lower:]')
export ARCH=$(uname -m)
curl -sfL "https://github.com/intelsdi-x/snap-plugin-publisher-file/releases/download/2/snap-plugin-publisher-file_${OS}_${ARCH}" -o snap-plugin-publisher-file
curl -sfL "https://github.com/intelsdi-x/snap-plugin-collector-psutil/releases/download/8/snap-plugin-collector-psutil_${OS}_${ARCH}" -o snap-plugin-collector-psutil
curl -sfL "https://github.com/intelsdi-x/snap-plugin-publisher-graphite/releases/download/5/snap-plugin-publisher-graphite_${OS}_${ARCH}" -o snap-plugin-publisher-graphite
curl -sfL "https://github.com/intelsdi-x/snap-plugin-collector-docker/releases/download/5/snap-plugin-collector-docker_${OS}_${ARCH}" -o snap-plugin-collector-docker
snaptel plugin load snap-plugin-publisher-file
snaptel plugin load snap-plugin-collector-psutil
snaptel plugin load snap-plugin-publisher-graphite
snaptel plugin load snap-plugin-collector-docker
# my local plugins
snaptel plugin load /vagrant_snap/processor/tag/sequence_processor.py
snaptel plugin load /vagrant_snap/processor/rolling_average/rolling_average_processor.py
# my tasks
snaptel task create -t /vagrant_snap/tasks/psutil_publish_to_graphite_task.yml
snaptel task create -t /vagrant_snap/tasks/sequence_and_publish_task.yml
snaptel task create -t /vagrant_snap/tasks/average_and_publish_task.yml
snaptel task create -t /vagrant_snap/tasks/average_and_publish_to_graphite_task.yml
snaptel task create -t /vagrant_snap/tasks/docker_publish_to_graphite_task.yml



