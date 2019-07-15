.PHONY: init install build lint test coverage fmt publish
.SILENT: init install build lint test coverage fmt publish

init: build lint test coverage

install:
	pip install --upgrade pip setuptools wheel && pip install .

build:
	pip install --upgrade pip setuptools wheel && pip install -e .[tests]

lint:
	isort -c -rc .
	black --check setup.py adz

test:
	pytest tests

coverage:
	pytest --cov-report=term --cov=adz tests

fmt:
	isort -rc .
	black setup.py adz tests

publish:
	pip install wheel twine
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
	rm -rf build dist adz.egg-info
