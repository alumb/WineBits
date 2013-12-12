package "python" 
package "unzip" 

remote_file "/home/vagrant/engine.zip" do
    source "http://googleappengine.googlecode.com/files/google_appengine_1.8.7.zip"
    action :create_if_missing
end

execute "unzip engine.zip" do
    cwd "/home/vagrant/"
    command "unzip engine.zip" 
    not_if { ::File.exists?("/home/vagrant/google_appengine")}
end
