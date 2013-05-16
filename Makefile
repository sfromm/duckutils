all: pep8

pep8:
	@echo 'Running PEP8 compliance tests'
	-pep8 -r duckutils
