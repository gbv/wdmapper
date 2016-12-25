.PHONY: test build clean docs

test:
	python setup.py test

build: docs
	python setup.py bdist_wheel --universal

release: clean build
	twine upload dist/*

clean:
	find . -name \*.pyc -or -name __pycache__ -exec rm -r -f '{}' ';'
	rm -rf *.egg *.egg-info
	rm -rf dist build

docs:
	rm -rf docs/api docs/_build
	sphinx-apidoc -fMeT -o docs/api wdmapper
	for f in docs/api/*.rst; do\
		perl -pi -e 's/(module|package)$$// if $$. == 1' $$f ;\
	done
	$(MAKE) -C docs html

requirements:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
