#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py: script showing an example of using this package
# Author: Ravi Joshi
# Date: 2018/10/01

# import modules
from whillpy import Whill, Power

whill = Whill(port='/dev/ttyUSB0')
whill.set_power(Power.On)
