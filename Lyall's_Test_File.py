"""
Created on Thu Mar 22 15:07:43 2018
@author: Tanvee
First attempt at an program for the EV3 bot.
The main aim of this is to develop an algorithm to searchclockwise for and identify
close objects, before rushing to meet them.
"""

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

tsRIGHT = TouchSensor(INPUT_3)
assert tsRIGHT.connected

tsLEFT = TouchSensor(INPUT_2)
assert tsLEFT.connected

us = UltrasonicSensor()
assert us.connected

cs = ColorSensor(INPUT_4)
assert cs.connected

print("All Connected");

# The gyro is reset when the mode is changed, so the first line is extra, just so we
# can change the mode the 'GYRO-ANGLE', which is what we want
# gs.mode = 'GYRO-RATE'  # Changing the mode resets the gyro
# gs.mode = 'GYRO-ANG'  # Set gyro mode to return compass angle

# We will need to check EV3 buttons state.
btn = Button()

# FUNCTION DEFINITIONS

def drive(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')

def main():
    print(btn.buttons_pressed)
    if(btn.left)
        stop()
    if(btn.right)
        print("The button was pressed")
        drive(100, -100)
        sleep(3)
        stop()



"""
    The default action is to spin around in an attempt to detect any object
    within a certain radius using the ultrasonic sensor.
    If the ultrasonic detects anything within 500mm the robot's reacts by "charging" at the object

"""


