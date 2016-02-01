#!/usr/bin/env python

from setuptools import setup

setup(
    name='wrapplog',
    version='0.1.0',
    py_modules=['wrapplog'],
    install_requires=[
        'structlog==15.0.0',
    ],
    zip_safe=False,
)
