#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

# Connect motors
rightMotor = LargeMotor(OUTPUT_C)

assert rightMotor.connected

leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected

btn = Button()


def drive(speed):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=speed)
    rightMotor.run_direct(duty_cycle_sp=speed)


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


for i in range(0, 100, 10):
    drive(i)
    sleep(5)
stop()

