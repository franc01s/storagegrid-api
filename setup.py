#!/usr/bin/env python

from distutils.core import setup
import sys


setup(name='storagegrid',
      version='0.0.1',
      description='API towards Netapp Stotagegrid admin node appliance',
      author='François Egger',
      author_email='francois@egger.cloud',
      url='https://github.com/franc01s/storagegrid-api',
      packages=['storagegrid'],
      classifiers=['Development Status :: 1 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: System :: Networking'],
      requires=[
          'requests'
      ]
      )
