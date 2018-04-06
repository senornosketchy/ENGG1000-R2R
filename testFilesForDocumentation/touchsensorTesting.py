#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

tsLEFT = TouchSensor(INPUT_3)
assert tsLEFT.connected

tsRIGHT = TouchSensor(INPUT_2)
assert tsRIGHT.connected

btn = Button()

while not btn.any():
    sleep(0.1)
    print("Left sensor:", tsLEFT.value())
    print("Right sensor:", tsRIGHT.value())
