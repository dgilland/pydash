#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


package_dir = 'src'
packages = find_packages(package_dir)


setup(
    package_dir={'': package_dir},
    packages=packages,
    include_package_data=True
)
