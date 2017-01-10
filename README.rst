multiset
========

This package provides a multiset_ implementation for python.

|pypi| |coverage| |build| |docs|

Overview
--------

A multiset is similar to the builtin set_, but it allows an element to occur multiple times.
It is an unordered collection of element which have to be hashable just like in a set_.
It supports the same methods and operations as set_ does, e.g. membership test, union, intersection, and
(symmetric) difference::

    >>> set1 = Multiset('aab')
    >>> set2 = Multiset('abc')
    >>> sorted(set1 | set2)
    ['a', 'a', 'b', 'c']

Multisets can be used in combination with sets_::

    >>> Multiset('aab') >= {'a', 'b'}
    True

Multisets are mutable::

    >>> set1.update('bc')
    >>> sorted(set1)
    ['a', 'a', 'b', 'b', 'c']

There is an immutable version similar to the frozenset_ which is also hashable::

    >>> set1 = FrozenMultiset('abc')
    >>> set2 = FrozenMultiset('abc')
    >>> hash(set1) == hash(set2)
    True
    >>> set1 is set2
    False

The implementation is based on a dict_ that maps the elements to their multiplicity in the multiset.
Hence, some dictionary operations are supported.

In contrast to the `collections.Counter`_ from the standard library, it has proper support for set
operations and only allows positive counts. Also, elements with a zero multiplicity are automatically
removed from the multiset.

Installation
------------

Installing `multiset` is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install multiset

Documentation
-------------

The documentation is available at `Read the Docs`_.

.. _`Read the Docs`: http://multiset.readthedocs.io/

API Documentation
.................

If you are looking for information on a particular method of the Multiset class, have a look at the
`API Documentation`_. It is automatically generated from the docstrings.

.. _`API Documentation`: http://multiset.readthedocs.io/en/latest/api.html

License
-------

Licensed under the MIT_ license.


.. _multiset: https://en.wikipedia.org/wiki/Multiset
.. _set: https://docs.python.org/3.5/library/stdtypes.html#set-types-set-frozenset
.. _sets: set_
.. _frozenset: set_
.. _dict: https://docs.python.org/3.5/library/stdtypes.html#mapping-types-dict
.. _`collections.Counter`: https://docs.python.org/3.5/library/collections.html#collections.Counter
.. _MIT: https://opensource.org/licenses/MIT


.. |pypi| image:: https://img.shields.io/pypi/v/multiset.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/multiset
    :alt: Latest version released on PyPi

.. |coverage| image:: https://coveralls.io/repos/github/wheerd/multiset/badge.svg?branch=master
    :target: https://coveralls.io/github/wheerd/multiset?branch=master
    :alt: Test coverage

.. |build| image:: https://travis-ci.org/wheerd/multiset.svg?branch=master
    :target: https://travis-ci.org/wheerd/multiset
    :alt: Build status of the master branch

.. |docs| image:: https://readthedocs.org/projects/multiset/badge/?version=latest
    :target: http://multiset.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
