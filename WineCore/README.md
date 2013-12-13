## WineCore ##

## Installing the GAE Vagrant Environment ##

0. Install Git
1. Install VirtualBox
2. Install Vagrant
3. Open the WineCore directory in a terminal (Git provides this on Windows).
4. `vagrant up`
5. `vagrant ssh`

## Makefile ##

    make run

Run the mock dev Google App Server on 0.0.0.0, port 8080 (8000 for admin server)

    make deploy

Deploy the whole shebang. 

    make runclean

Like 'run', but clears out the DB first. Important note: 
this won't clear any of the search documents created by WineTruth. 

