package "unzip" 

remote_file "/home/vagrant/sencha.zip" do
    source "http://cdn.sencha.com/cmd/4.0.2.67/SenchaCmd-4.0.2.67-linux-x64.run.zip"
    action :create_if_missing
end

execute "unzip sencha.zip" do
    cwd "/home/vagrant/"
    command "unzip sencha.zip" 
    not_if { ::File.exists?("/home/vagrant/SenchaCmd-4.0.2.67-linux-x64.run")}
end

file "/home/vagrant/SenchaCmd-4.0.2.67-linux-x64.run" do
  mode "0755"
end

execute "install SenchaCmd" do
    cwd "/home/vagrant/"
    command "./SenchaCmd-4.0.2.67-linux-x64.run --mode unattended --prefix /home/vagrant" 
    not_if { ::File.directory?("/home/vagrant/Sencha")}
end

execute "install missing fontconfig package" do
    cwd "/home/vagrant/"
    command "sudo aptitude install fontconfig" 
end

execute "fixup /home/vagrant/Sencha permissions" do
  command "chown -Rf vagrant.vagrant /home/vagrant/Sencha"
  only_if { Etc.getpwuid(File.stat('/home/vagrant/Sencha').uid).name != "vagrant" }
end

execute "Add to path" do
    cwd "/home/vagrant/"
    command "export PATH=$PATH:/home/vagrant/Sencha/Cmd/4.0.2.67/" 
end
