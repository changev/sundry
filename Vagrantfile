######################
# Vagrant File Start #
######################

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    
    # MONORAIL SERVER
    config.vm.define "dev" do |target|
        target.vm.box = "rackhd/rackhd"
        target.vm.box_version = "0.15"
        target.vm.provider "virtualbox" do |v|
            v.memory = 4096
            v.cpus = 4
            v.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
        end

        # Create a public network, which generally matched to bridged network.
        # Bridged networks make the machine appear as another physical device on
        # your network.
        # target.vm.network :public_network
        if ENV['WORKSPACE']
          target.vm.synced_folder "#{ENV['WORKSPACE']}/build-deps", "/home/vagrant/src/"
          target.vm.synced_folder "#{ENV['WORKSPACE']}/build-config", "/home/vagrant/src/build-config/"
          if ENV['REPO_NAME']
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/#{ENV['REPO_NAME']}"
          end
          if ENV['REPO_NAME'] == "on-tasks"
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-taskgraph/node_modules/on-tasks/" 
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-http/node_modules/on-tasks/" 
          end
          if ENV['REPO_NAME'] == "on-core"
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-taskgraph/node_modules/on-core/"  
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-http/node_modules/on-core/" 
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-tftp/node_modules/on-core/" 
            target.vm.synced_folder "#{ENV['WORKSPACE']}/build", "/home/vagrant/src/on-dhcp-proxy/node_modules/on-core/" 
          end
        end
        
        if ENV['CONFIG_DIR'] # this ENV VAR defined in on-build-config repo's test.sh, pointing to vagrant/config/mongo/config.json in on-build-config repo.
          target.vm.synced_folder "#{ENV['WORKSPACE']}/#{ENV['CONFIG_DIR']}", "/opt/monorail/"
          target.vm.synced_folder "#{ENV['WORKSPACE']}/#{ENV['CONFIG_DIR']}", "/opt/onrack/etc/"
          target.vm.synced_folder "#{ENV['WORKSPACE']}/#{ENV['CONFIG_DIR']}", "/home/vagrant/opt/monorail/"
        end
        
        if ENV['TEST_GROUP']
          if ENV['TEST_GROUP'] == "esxi-5-5-install.v1.1.test"
            config.vm.provision "file", source: "./dhcpd.conf", destination: "~/dhcpd.conf"
            config.vm.provision "shell" do |s|
            s.inline = "cp /home/vagrant/dhcpd.conf /etc/dhcp"
            s.privileged = true
            end
          end
        end
        target.vm.network "public_network", ip: "172.31.128.1", bridge: "em1"
        target.vm.network "forwarded_port", guest: 8080, host: 9090
        target.vm.network "forwarded_port", guest: 5672, host: 9091
        target.vm.network "forwarded_port", guest: 9080, host: 9092
        target.vm.network "forwarded_port", guest: 8443, host: 9093

        # If true, then any SSH connections made will enable agent forwarding.
        # Default value: false
        target.ssh.forward_agent = true

        target.vm.provision "shell", inline: <<-SHELL
          service isc-dhcp-server start
          service rsyslog stop
          echo manual | sudo tee /etc/init/rsyslog.override
          nf start > /home/vagrant/src/"#{ENV['REPO_NAME']}"/vagrant.log &
        SHELL
    end
end
