"""
pydash
======

Python port of Lodash.

Project: https://github.com/dgilland/pydash
"""

from setuptools import setup


meta = {}
with open('pydash/__meta__.py') as fp:
    exec(fp.read(), meta)


setup(
    name=meta['__title__'],
    version=meta['__version__'],
    url=meta['__url__'],
    license=meta['__license__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description=meta['__summary__'],
    long_description=__doc__,
    packages=['pydash'],
    install_requires=[],
    test_suite='tests',
    keywords='lodash underscore functional',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ]
)
