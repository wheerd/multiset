@ECHO off
if /I %1 == init goto :init
if /I %1 == test goto :test
if /I %1 == stubtest goto :stubtest
if /I %1 == check goto :check
if /I %1 == coverage goto :coverage
if /I %1 == build goto :build

goto :eof

:init
	pip install -r dev-requirements.txt
goto :eof

:test
	py.test tests\ --doctest-modules multiset README.rst
goto :eof


:stubtest
	python -m mypy.stubtest multiset
goto :eof

:check
	pylint multiset
goto :eof

:coverage
	py.test --cov=multiset --cov-report lcov --cov-report term-missing tests/
goto :eof

:build
	python -m build
goto :eof