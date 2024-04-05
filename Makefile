init:
	pip install -r dev-requirements.txt

test:
	py.test tests/ --doctest-modules multiset README.rst

stubtest:
	python -m mypy.stubtest multiset

check:
	pylint multiset

coverage:
	py.test --cov=multiset --cov-report lcov --cov-report term-missing tests/

build:
	python -m build
