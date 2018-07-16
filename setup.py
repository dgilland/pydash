#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


package_dir = 'src'
packages = find_packages(package_dir)

version = {}
with open('{}/{}/__version__.py'.format(package_dir, packages[0])) as f:
    exec(f.read(), version)


setup(
    version=version['__version__'],
    package_dir={'': package_dir},
    packages=packages,
    include_package_data=True
)
