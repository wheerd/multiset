init:
	pip install -r dev-requirements.txt

test:
	py.test tests/ --doctest-modules multiset.py README.rst

check:
	pylint multiset

coverage:
	coverage run --source multiset -m py.test
	coverage report -m
