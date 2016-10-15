init:
	pip install -r requirements.txt

test:
	python -m unittest test_multiset

check:
	pylint multiset

coverage:
	coverage run --source multiset.py -m test_multiset
	coverage html
