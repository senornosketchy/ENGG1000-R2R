#!/usr/bin/python3

from ev3dev.ev3 import *

us = UltrasonicSensor()
assert us.connected

btn = Button()

while not btn.any():
    print(us.value())
