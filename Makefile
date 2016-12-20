.PHONY: test build clean

test:
	python setup.py test

build:
	python setup.py bdist_wheel

release: clean build
	twine upload dist/*

clean:
	find . -name \*.pyc -delete
	rm -rf dist
