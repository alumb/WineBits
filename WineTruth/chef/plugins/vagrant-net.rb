# borrowed from https://gist.github.com/2050259 and http://johntdyer.com/blog/2013/01/25/ohai/

# If the vagrant user exists we're running on Vagrant.  Not checking virtualization provider as Vagrant 1.1+ supports multiple.

provide "ipaddress"
require_plugin "#{os}::network"
require_plugin "passwd"

if etc["passwd"].any? { |k,v| k == "vagrant"}
  if network["interfaces"]["eth1"]
    network["interfaces"]["eth1"]["addresses"].each do |ip, params|
      if params['family'] == ('inet')
        Chef::Log.info("vagrant-ohai-plugin - forcing :ipaddress to #{ip}")
        ipaddress ip
      end
    end
  else
    Chef::Log.debug("vagrant-ohai-plugin - eth1 not detected")
  end
else
  Chef::Log.debug("vagrant-ohai-plugin - Vagrant not detected")
end
