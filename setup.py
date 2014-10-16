"""
pydash
======

A utility library for doing "stuff" in a functional way. Based on the
`Lo-Dash <http://lodash.com/>`_  Javascript library.

Project: https://github.com/dgilland/pydash

Documentation: http://pydash.readthedocs.org/
"""

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


meta = {}
exec(read('pydash/__meta__.py'), meta)


class Tox(TestCommand):
    user_options = [
        ('tox-args=', 'a', "Arguments to pass to tox")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = '-c tox.ini'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here because outside the eggs aren't loaded.
        import tox
        import shlex

        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


setup(
    name=meta['__title__'],
    version=meta['__version__'],
    url=meta['__url__'],
    license=meta['__license__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description=meta['__summary__'],
    long_description=read('README.rst'),
    packages=find_packages(exclude=['tests']),
    install_requires=meta['__install_requires__'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    test_suite='tests',
    keywords='utility functional lodash underscore',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
