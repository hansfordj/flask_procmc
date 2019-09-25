#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To use a consistent encoding
from os import path
from codecs import open
# Always prefer setuptools over distutils
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'flask-procmc',
    packages = ['flask-procmc'],
    version = '0.0.1',
    description = 'A python wrapper around the pro.coinmarketcap.com API for flask.',
    author = 'Jordan Hansford',
    author_email = 'hansfordjordan@gmail.com',
    url = 'https://github.com/hansfordj/flask_procmc',
    project_urls={
        'Bug Reports': 'https://github.com/hansfordj/flask_procmc/issues',
        'Buy me a coffee': 'https://github.com/barnumbirr/coinmarketcap#buy-me-a-coffee',
    },
    license = 'Apache v2.0 License',
    install_requires=[
    'requests>=2.18.4',
    'requests_cache>=0.4.13'
    ],
    keywords = ['cryptocurrency', 'API', 'coinmarketcap','BTC', 'Bitcoin', 'LTC', 'Litecoin', 'XMR', 'Monero', 'ETH', 'Ethereum '],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description = long_description,
    long_description_content_type='text/markdown',
)
