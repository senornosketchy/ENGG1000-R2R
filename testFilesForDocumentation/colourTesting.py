#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

cs = ColorSensor()
assert cs.connected

btn = Button()

while not btn.any():
    sleep(0.1)
    print(cs.value())
