#!/usr/bin/python3

from ev3dev.ev3 import *

cs = ColorSensor()
assert cs.connected

gy.mode = 'GYRO-ANG'

btn = Button()

while not btn.any():
    print(gy.value())
