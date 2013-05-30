#!/usr/bin/env python

import os
import sys

from duckutils import __version__, __author__, __name__
from distutils.core import setup

setup(name=__name__,
      version=__version__,
      author=__author__,
      author_email='sfromm@gmail.com',
      url='https://github.com/sfromm/duckutils',
      license='GPLv3',
      install_requires=['PyYaml'],
      package_dir={'duckutils': 'duckutils'},
      packages=['duckutils']
      )
