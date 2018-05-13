#!/usr/bin/python3

from ev3dev.ev3 import *

rightMotor = LargeMotor(OUTPUT_A)
assert rightMotor.connected

leftMotor = LargeMotor(OUTPUT_D)
assert leftMotor.connected


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')

stop()