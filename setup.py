# -*- coding: utf-8 -*-
import os.path

from setuptools import setup

root = os.path.dirname(__file__)

with open(os.path.join(root, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(root, 'LICENSE')) as f:
    license = f.read()

setup(
    name='multiset',
    use_scm_version=True,
    description='An implementation of a multiset.',
    long_description=readme,
    author='Manuel Krebber',
    author_email='admin@wheerd.de',
    url='https://github.com/wheerd/multiset',
    license='MIT',
    zip_safe=True,
    py_modules=['multiset'],
    test_suite='test_multiset',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    setup_requires=[
        'setuptools_scm >= 1.7.0'
    ],
    tests_require=[
        'ddt'
    ],
    extras_require={
        ':python_version == "3.3"': 'typing >= 3.5',
        ':python_version == "3.4"': 'typing >= 3.5'
    }
)

