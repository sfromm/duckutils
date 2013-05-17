all: clean python

clean:
	@echo 'Cleaning up'
	rm -rf build
	rm -rf dist
	find . -type f -regex ".*\.py[co]$$" -delete

python:
	python setup.py build

install:
	python setup.py install

sdist:
	python setup.py sdist -t MANIFEST.in

pep8:
	@echo 'Running PEP8 compliance tests'
	-pep8 -r --ignore=E302 duckutils
