# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

config.vm.box = "ubuntu/xenial64"
config.vm.synced_folder "./", "/vagrant_snap"

# Manage any proxy on the host
if Vagrant.has_plugin?("vagrant-proxyconf")
if ENV['http_proxy'] && !ENV['http_proxy'].empty?
    config.proxy.http     = ENV['http_proxy']
    config.git_proxy.http = ENV['http_proxy']
end
if ENV['https_proxy'] && !ENV['https_proxy'].empty?
    config.proxy.https    = ENV['https_proxy']
end
if ENV['no_proxy'] && !ENV['no_proxy'].empty?
    config.proxy.no_proxy = ENV['no_proxy'] + ",192.168.16.6"
end
end
# Provider-specific configuration so you can fine-tune various
# backing providers for Vagrant. These expose provider-specific options.
# Example for VirtualBox:
#
config.vm.provider "virtualbox" do |vb|
  # Customize the amount of memory on the VM:
  vb.memory = "1024"
  vb.cpus = "1"
end

pukka_ip = "192.168.16.6"
config.vm.define "pukka" do |pukka|
    pukka.vm.hostname = "pukka"
    pukka.vm.network "private_network", ip: pukka_ip
    pukka.vm.provision "shell", preserve_order: true, path: "provisioning/install.sh", env: {"BIND_IP" => pukka_ip, "SEED_IP" => pukka_ip}
end

config.vm.define "typhoo" do |typhoo|
    typhoo_ip = "192.168.16.7"
    typhoo.vm.hostname = "typhoo"
    typhoo.vm.network "private_network", ip: "192.168.16.7"
    typhoo.vm.provision "shell", preserve_order: true, path: "provisioning/install.sh", env: {"BIND_IP" => typhoo_ip, "SEED_IP" => pukka_ip}
    typhoo.vm.provision "shell", path: "provisioning/install_graphite.sh"
    typhoo.vm.provision "shell", preserve_order: true, path: "provisioning/start_tasks.sh"
end

end
