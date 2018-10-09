#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup.py: script to facilitate installation of the package
# Author: Ravi Joshi
# Date: 2018/10/02

# import modules
from setuptools import setup, find_packages

setup(name='whillpy',
      version='0.1',
      description='Unofficial python package for WHILL Model CK control',
      url='http://github.com/ShibataLab/whillpy',
      author='Ravi Prakash Joshi',
      author_email='joshi.ravi-prakash869@mail.kyutech.jp',
      license='MIT',
      packages=find_packages(),
      install_requires=['pyserial'],
      )
