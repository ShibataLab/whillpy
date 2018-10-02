#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py: script showing an example of using this package
# Author: Ravi Joshi
# Date: 2018/10/01

# import modules
from whillpy import Whill, Power

# initialize Whill by providing the name of serial port
whill = Whill(port='/dev/ttyUSB0')

# control the power
whill.set_power(Power.On)

# move straight while turning left
whill.move(straight=10, turn=-50)
