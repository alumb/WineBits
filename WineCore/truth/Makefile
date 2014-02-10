install:
	pip install -r deps

test:
	python `which nosetests`

random_wine:
	echo "Make sure to turn on the server first!" 
	python http_wine_load.py http://localhost:8081

lint:
	pep8

todo:
	ack-grep 'TODO' -i --nomake
