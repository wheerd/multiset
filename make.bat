@ECHO off
if /I %1 == init goto :init
if /I %1 == test goto :test
if /I %1 == check goto :check
if /I %1 == coverage goto :coverage

goto :eof

:init
	pip install -r dev-requirements.txt
goto :eof

:test
	py.test test_multiset.py --doctest-modules multiset.py README.rst
goto :eof

:check
	pylint multiset
goto :eof

:coverage
	py.test --cov=multiset --cov-report html --cov-report term test_multiset.py
goto :eof
