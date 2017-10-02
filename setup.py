#! /usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

extra_files = [] 
extra_files.append(os.path.join(here, 'CONTRIBUTORS'))
extra_files.append(os.path.join(here, 'LICENSE'))
extra_files.append(os.path.join(here, 'README.rst'))
extra_files.append(os.path.join(here, 'requirements.txt'))
extra_files.append(os.path.join(here, 'VERSION'))

with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name='gitsieve',
    packages=find_packages(),
    package_data={'': extra_files},
    install_requires=required,
    version=version,
    description='',
    author='Blaise Thompson',
    author_email='blaise@untzag.com',
    license='MIT',
    url='https://github.com/untzag/gitsieve',
    keywords='',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Development Status :: 1 - Planning',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5']
)
