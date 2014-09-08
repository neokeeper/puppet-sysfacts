VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  {
    :Centos65_64 => {
      :box     => 'centos65_64',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/centos-65-x64-virtualbox-puppet.box',
    },
    :Centos64_64 => {
      :box     => 'centos64_64',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/centos-64-x64-vbox4210.box',
    },
    :Centos6_64 => {
      :box     => 'centos6_64',
      :box_url => 'https://saleseng.s3.amazonaws.com/boxfiles/CentOS-6.3-x86_64-minimal.box',
    },
    :Centos63_64 => {
      :box     => 'centos-6.3-64bit',
      :box_url => 'http://packages.vstone.eu/vagrant-boxes/centos-6.3-64bit-latest.box',
    },
    :Centos510_64 => {
      :box     => 'centos-5.10-64bit',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/centos-510-x64-virtualbox-puppet.box',
    },
    :Centos58_64 => {
      :box     => 'centos-5.8-64bit',
      :box_url => 'http://packages.vstone.eu/vagrant-boxes/centos-5.8-64bit-latest.box',
    },
    :Ubuntu1404_64 => {
      :box     => 'trusty-server-cloudimg-amd64-vagrant-disk1.box',
      :box_url => 'https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box',
    },
    :Ubuntu1304_64 => {
      :box     => 'raring64',
      :box_url => 'http://cloud-images.ubuntu.com/vagrant/raring/current/raring-server-cloudimg-amd64-vagrant-disk1.box',
    },
    :Ubuntu1210_64 => {
      :box     => 'quantal64',
      :box_url => 'http://cloud-images.ubuntu.com/vagrant/quantal/current/quantal-server-cloudimg-amd64-vagrant-disk1.box',
    },
    :Ubuntu1204 => {
      :box     => 'ubuntu-server-12042-x64-vbox4210',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-server-12042-x64-vbox4210.box',
    },
    :Ubuntu1004 => {
      :box     => 'ubuntu-server-12042-x64-vbox4210',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-server-12042-x64-vbox4210.box',
    },
    :Debian7 => {
      :box     => 'debian-70rc1-x64-vbox4210',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/debian-70rc1-x64-vbox4210.box',
    },
    :Debian6 => {
      :box     => 'debian-607-x64-vbox4210',
      :box_url => 'http://puppet-vagrant-boxes.puppetlabs.com/debian-607-x64-vbox4210.box',
    },
  }.each do |name, cfg|
    config.vm.define name do |local|
      local.vm.box       = cfg[:box]
      local.vm.box_url    = cfg[:box_url]
      local.vm.host_name  = ENV['VAGRANT_HOSTNAME'] || name.to_s.downcase.gsub(/_/, '-').concat(".puppetlabs.vm")

      local.vm.network :forwarded_port, guest: 80, host: 8080, protocol: 'tcp', auto_correct: true

      # Puppet Provisioner setup
      local.vm.provision :puppet do |puppet|
        puppet.manifests_path     = "manifests"
        puppet.module_path        = "modules"
        puppet.manifest_file      = "site.pp"
        puppet.working_directory  = '/vagrant'
        puppet.options            = [
         '--verbose',
         '--report',
         '--show_diff',
         '--pluginsync',
         '--summarize',
         #'--evaltrace',
         #'--trace',
         #'--debug',
        ]
      end
    end
  end
end
