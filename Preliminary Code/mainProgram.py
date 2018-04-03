from time import sleep
import sys, os

# Import the ev3dev specific library
from ev3dev.ev3 import *

# Connect motors
rightMotor = LargeMotor(OUTPUT_C)

assert rightMotor.connected

leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected

# Connect sensors

us = UltrasonicSensor()

cs = ColorSensor(INPUT_4)

gs = GyroSensor()

gs.mode = 'GYRO-ANG'  # Set gyro mode to return compass angle

# Declaring buttons
btn = Button()


# Basic movement control
def drive(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


# Spinning the robot, clockwise/anticlockwise depending on required direction
def search(spinDirection):
    drive(direction * -100, direction * 100)


# Stop both motors
def stop():
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


"""
    The default action is to spin around in an attempt to detect any object
    within a certain radius using the ultrasonic sensor.
    If the ultrasonic detects anything within 750mm the robot's reacts by "charging" at the object

"""


def startSequence(spinDirection):
    sleep(3)
    while gs.value() < 150:
        search(spinDirection)
        if us.value < 750:
            drive(100, 100)

# Stop the motors before exiting.
stop()
