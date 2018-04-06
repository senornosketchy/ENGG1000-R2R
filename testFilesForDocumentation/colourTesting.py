#!/usr/bin/python3

from ev3dev.ev3 import *

cs = ColorSensor()
assert cs.connected

btn = Button()

while not btn.any():
    print(cs.value())
