# Import a few system libraries that will be needed
from time import sleep
import sys, os
import matplotlib.pyplot as plt

# Import the ev3dev specific library
from ev3dev.ev3 import *

# Connect motors
rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_C)

# Connect touch sensors.

us = UltrasonicSensor();
assert us.connected

# We will need to check EV3 buttons state.
btn = Button()


def start(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


# Run the robot until a button is pressed.

while not btn.on_down:
    if btn.on_up:
        print("The ultrasonic value is:", us.value())
