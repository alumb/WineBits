install:
	pip install -r deps

run:
	~/google_appengine/dev_appserver.py . --host=0.0.0.0 

runclean:
	~/google_appengine/dev_appserver.py . --host=0.0.0.0 --clear_datastore=yes

test:
	python `which nosetests`

lint:
	pep8

todo:
	ack-grep 'TODO' -i --nomake
