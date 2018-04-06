#!/usr/bin/python3

from time import sleep
from ev3dev.ev3 import *

gy = GyroSensor()
assert gy.connected

gy.mode = 'GYRO-ANG'

btn = Button()

while not btn.any():
    sleep(0.1)
    print(gy.value())
