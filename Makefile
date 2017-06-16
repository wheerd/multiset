init:
	pip install -r dev-requirements.txt

test:
	py.test tests/ --doctest-modules multiset.py README.rst

check:
	pylint multiset

coverage:
	py.test --cov=multiset --cov-report html --cov-report term tests/
