#!/usr/bin/env python

from distutils.core import setup
import pkg_resources

# You need to have python-bert installed first.
version = pkg_resources.get_distribution("bert").version

# The original author of this library is
# Ken Robertson ken@invalidlogic.com
# This version is a fork on github maintained by
# Tyler Neylon tyler@zillabyte.com.
setup(
    name = 'ernie',
    version = version,
    description = 'BERT-Ernie Library',
    author = 'Tyler Neylon',
    author_email = 'tyler@zillabyte.com',
    url = 'https://github.com/tylerneylon/python-ernie',
    packages = ['ernie'],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
