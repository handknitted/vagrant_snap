# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

config.vm.box = "ubuntu/xenial64"
config.vm.hostname = "pukka"

# Create a forwarded port mapping which allows access to a specific port
# within the machine from a port on the host machine. In the example below,
# accessing "localhost:8080" will access port 80 on the guest machine.
# config.vm.network "forwarded_port", guest: 80, host: 8080

config.vm.network "private_network", ip: "192.168.16.6"
# Create a public network, which generally matched to bridged network.
# Bridged networks make the machine appear as another physical device on
# your network.
# config.vm.network "public_network"

# Share an additional folder to the guest VM. The first argument is
# the path on the host to the actual folder. The second argument is
# the path on the guest to mount the folder. And the optional third
# argument is a set of non-required options.
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
  
  # Just in case the virtualbox gui is started - TODO do I need this if the hostname is set?
  #vb.name = "pukka"

  # Customize the amount of memory on the VM:
  vb.memory = "8192"
  vb.cpus = "2"
end


#  install dependencies for our process
config.vm.provision "shell", path: "install.sh"
# provision the environments


end
