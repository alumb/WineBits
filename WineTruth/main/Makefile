install:
	pip install -r deps

run:
	~/google_appengine/dev_appserver.py . --host=0.0.0.0 

test:
	python `which nosetests`

lint:
	pep8

todo:
	ack-grep 'TODO' -i --nomake
