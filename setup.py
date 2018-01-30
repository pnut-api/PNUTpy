#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='pnutpy',
      version='0.2.2',
      description='pnut.io API library for python',
      long_description=open('README.rst').read(),
      license='MIT',
      author='33MHz, pnut.io',
      author_email='support@pnut.io',
      url='https://github.com/pnut-api/PNUTpy',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'python-dateutil>=2.2',
          'requests>=2.4.3',
      ],
      keywords='pnut.io api library',
      zip_safe=True)
