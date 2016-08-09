./packages:
	virtualenv packages
	. packages/bin/activate && pip install -r requirements.txt

dependencies: ./packages

functional:
	. packages/bin/activate && nosetests test.functional
