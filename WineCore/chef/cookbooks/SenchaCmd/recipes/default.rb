#package "java" 
package "unzip" 

remote_file "/home/vagrant/sencha.zip" do
    source "http://cdn.sencha.com/cmd/4.0.1.45/SenchaCmd-4.0.1.45-linux.run.zip"
    action :create_if_missing
end

execute "unzip sencha.zip" do
    cwd "/home/vagrant/"
    command "unzip sencha.zip" 
    not_if { ::File.exists?("/home/vagrant/SenchaCmd-4.0.1.45-linux.run")}
end

file "/home/vagrant/SenchaCmd-4.0.1.45-linux.run" do
  mode "0755"
end

execute "install SenchaCmd" do
    cwd "/home/vagrant/"
    command "./SenchaCmd-4.0.1.45-linux.run --mode unattended --prefix /home/vagrant" 
end