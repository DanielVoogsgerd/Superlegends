#!/usr/bin/env python

from time import sleep

import Superlegends


spl = Superlegends.Superlegends()
try:
    spl.connect('10.0.1.30')
    spl.on()
    spl.setColor(255, 255, 255)
    sleep(1)
    spl.warm(100)
    sleep(1)
    spl.warm(255)
    sleep(1)
    spl.warm(30)
    sleep(1)

    spl.off()
    spl.disconnect()
except OSError as msg:
    spl.disconnect()
    print('There was a problem')
    print(msg)
