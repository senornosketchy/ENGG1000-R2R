#!/usr/bin/python3

from ev3dev.ev3 import *

rightMotor = LargeMotor(OUTPUT_C)
assert rightMotor.connected

leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')

stop()