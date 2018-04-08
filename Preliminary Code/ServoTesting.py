#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

# Connect motors
rightMotor = ServoMotor(OUTPUT_C)

btn = Button()


def drive(speed):
    """
    Start both motors at the given speeds.
    """
    rightMotor.COMMAND_RUN(position_sp=speed)


def stop():
    # Stop both motors
    rightMotor.stop(stop_action='brake')


for i in range(0, 100, 10):
    drive(i)
    sleep(1)
stop()

