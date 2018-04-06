#!/usr/bin/python3

# -----------------------------------------------------------------------------
# Copyright (c) 2015 Denis Demidov <dennis.demidov@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

# In this demo an Explor3r robot with touch sensor attachment drives
# autonomously. It drives forward until an obstacle is bumped (determined by
# the touch sensor), then turns in a random direction and continues. The robot
# slows down when it senses obstacle ahead (with the infrared sensor).
#
# The program may be stopped by pressing any button on the brick.
#
# This demonstrates usage of motors, sound, sensors, buttons, and leds.

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

print("1")

# Connect motors
rightMotor = LargeMotor(OUTPUT_C)

print("1.5")

assert rightMotor.connected

print("2")

leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected

# Connect sensors

print("2")

tsRIGHT = TouchSensor(INPUT_3)
assert tsRIGHT.connected

print("3")

tsLEFT = TouchSensor(INPUT_3)
assert tsLEFT.connected

print("4")

us = UltrasonicSensor()

print("5")

cs = ColorSensor(INPUT_4)

# The gyro is reset when the mode is changed, so the first line is extra, just so we
# can change the mode the 'GYRO-ANGLE', which is what we want
# gs.mode = 'GYRO-RATE'  # Changing the mode resets the gyro
# gs.mode = 'GYRO-ANG'  # Set gyro mode to return compass angle

# We will need to check EV3 buttons state.
btn = Button()


# Basic movement, controlling th power of left and right motors


def drive(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def searchclockwise():
    drive(-100, 100)


def searchanticlockwise():
    drive(100, -100)


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


"""
    The default action is to spin around in an attempt to detect any object
    within a certain radius using the ultrasonic sensor.
    If the ultrasonic detects anything within 500mm the robot's reacts by "charging" at the object
    
"""
print(5)
searchclockwise()
while not btn.any():
    print(us.value)
    if us.value() < 500 and cs.value() > 40:
        drive(100, 100)
    elif tsLEFT.value() and not tsRIGHT.value():
        drive(100, 80)
    elif tsRIGHT.value() and not tsLEFT.value():
        drive(80, 100)
    elif tsRIGHT.value() and tsLEFT.value():
        drive(100, 100)
    elif cs.value() < 40:
        drive(100, 100)
    else:
        searchclockwise()
# Stop the motors before exiting.
stop()
