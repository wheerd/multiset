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
	python -m unittest test_multiset
goto :eof

:check
	pylint multiset
goto :eof

:coverage
	coverage run --source multiset.py -m test_multiset
	coverage html
goto :eof
