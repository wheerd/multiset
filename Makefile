init:
	pip install -r dev-requirements.txt

test:
	py.test test_multiset --doctest-modules multiset README.rst

check:
	pylint multiset

coverage:
	py.test --cov=multiset --cov-report html --cov-report term test_multiset
