#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

us = UltrasonicSensor()
assert us.connected

btn = Button()

while not btn.any():
    sleep(0.1)
    print(us.value()/10, "cm")
