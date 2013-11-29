package "python-pip"

execute "install virtualenv" do
    command "pip install virtualenv" 
end 

execute "create virtualenv" do
    cwd "/home/vagrant/"
    command "virtualenv . --system-site-packages" 
end

file "/home/vagrant/.bash_profile" do
    content "source /home/vagrant/bin/activate"
    owner "vagrant"
    action :create
end

execute "install packages" do
    cwd "/home/vagrant/synced/main/"
    command "pip install -r deps" 
end

