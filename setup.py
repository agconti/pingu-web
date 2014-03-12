# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pingu
version = pingu.__version__

setup(
    name='pingu-web',
    version=version,
    author='',
    author_email='conti@fueled.com',
    packages=[
        'pingu',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['pingu/manage.py'],
)