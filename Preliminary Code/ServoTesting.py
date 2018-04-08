#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

# Connect motors
rightMotor = ServoMotor(OUTPUT_C)

assert rightMotor.connected

btn = Button()


def drive(speed):
    """
    Start both motors at the given speeds.
    """
    rightMotor.run_direct(duty_cycle_sp=speed)


def stop():
    # Stop both motors
    rightMotor.stop(stop_action='brake')


for i in range(0, 100, 10):
    drive(i)
    sleep(5)
stop()

