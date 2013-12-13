install:
	pip install -r deps

test:
	python `which nosetests`

random_wine:
	echo "Make sure to turn on the server first!" 
	python http_wine_load.py http://localhost:8080 random

sample_wine:
	echo "Make sure to turn on the server first!"
	python http_wine_load.py http://localhost:8080 data/wine_sample.json 

lint:
	pep8

todo:
	ack-grep 'TODO' -i --nomake
