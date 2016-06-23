#!/usr/bin/env python

from time import sleep

import Superlegends

spl = Superlegends.Superlegends()
spl.connect('127.0.0.1')
spl.turnOn()
spl.setColor(255, 255, 255)
sleep(1)
spl.warm(100)
sleep(1)
spl.warm(255)
sleep(1)
spl.warm(30)
sleep(1)

spl.turnOff()
