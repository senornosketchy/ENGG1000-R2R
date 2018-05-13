#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

us = UltrasonicSensor(INPUT_2)
assert us.connected

btn = Button()

while not btn.any():
    sleep(0.1)
    print(us.value(), "mm")
