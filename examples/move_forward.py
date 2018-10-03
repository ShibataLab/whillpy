#!/usr/bin/env python
# -*- coding: utf-8 -*-

# move_forward.py
# Author: Ravi Joshi
# Date: 2018/10/03

# import modules
import time
import whillpy

# initialize Whill by providing the name of the serial port
whill = whillpy.connect(port='/dev/ttyUSB0')

# move straight for defined steps
steps = 10
for _ in range(steps):
    whill.move(straight=10, turn=0)
    time.sleep(0.2)
