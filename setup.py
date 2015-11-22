#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="adnpy",
      version='0.3.9',
      description="App.net API library for python",
      long_description=open('README.rst').read(),
      license="MIT",
      author="Alex Kessinger, Bryan Berg, Mark Thurman, App.net",
      author_email="alex@app.net",
      url="https://github.com/appdotnet/ADNpy",
      packages=find_packages(exclude=['tests']),
      data_files=[('examples', ['examples/send-broadcast.py'])],
      install_requires=[
          'python-dateutil>=2.2',
          'requests>=2.4.3',
      ],
      keywords="app.net api library",
      zip_safe=True)
