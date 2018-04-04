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

cs = ColorSensor()

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
    drive(spinDirection * -100, spinDirection * 100)


# Stop both motors
def stop():
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')

# Basic Start sequence
def start_sequence(spinDirection):
    sleep(3)
    Sound.speak('')
    while gs.value() < 150:
        search(spinDirection)
        if us.value < 750 and cs.value() > 30:
            drive(100, 100)
        else:
            search(spinDirection)

# If the robot cannot see the other bot after the starting sequence
def lost():
    # If robot cannot find object drive forward to boundary then do another check
    # Below loop, keeps the robot driving back and forth till target is found.
    while cs.value() > 30:
        drive(-80, -80)
    # Didn't know the code, to make it spin 180 degrees.

while not btn.any():
    cs.mode = 'COL-REFLECT'
    start_sequence(spinDirection)
