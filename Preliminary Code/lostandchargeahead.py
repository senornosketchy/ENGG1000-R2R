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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

# In this demo an Explor3r robot with touch sensor attachement drives
# autonomously. It drives forward until an obstacle is bumped (determined by
# the touch sensor), then turns in a random direction and continues. The robot
# slows down when it senses obstacle ahead (with the infrared sensor).
#
# The program may be stopped by pressing any button on the brick.
#
# This demonstrates usage of motors, sound, sensors, buttons, and leds.

from time import sleep
import sys, os

from ev3dev.ev3 import *

# Connect motors
rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_C)

# Connect touch sensors.
ts1 = TouchSensor(INPUT_1)
assert ts1.connected
ts4 = TouchSensor(INPUT_4)
assert ts4.connected
us = UltrasonicSensor()
assert us.connected
gs = GyroSensor()
assert gs.connected
cs = ColorSensor()
assert gs.connected

gs.mode = 'GYRO-RATE'  # Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'  # Set gyro mode to return compass angle

# We will need to check EV3 buttons state.
btn = Button()


def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `speed_sp` attribute.
    """
    rightMotor.run_direct(duty_cycle_sp=75)
    leftMotor.run_direct(duty_cycle_sp=75)


def backup():
    """
    Back away from an obstacle.
    """

    # Sound backup alarm.
    Sound.tone([(1000, 500, 500)] * 3)

    # Turn backup lights on:
    Leds.set_color(Leds.RIGHT, Leds.RED)
    Leds.set_color(Leds.LEFT, Leds.RED)

    # Stop both motors and reverse for 1.5 seconds.
    # `run-timed` command will return immediately, so we will have to wait
    # until both motors are stopped before continuing.
    rightMotor.stop(stop_action='brake')
    leftMotor.stop(stop_action='brake')
    rightMotor.run_timed(speed_sp=-500, time_sp=1500)
    leftMotor.run_timed(speed_sp=-500, time_sp=1500)

    # When motor is stopped, its `state` attribute returns empty list.
    # Wait until both motors are stopped:
    while any(m.state for m in (leftMotor, rightMotor)):
        sleep(0.1)

    # Turn backup lights off:
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    Leds.set_color(Leds.LEFT, Leds.GREEN)


def turn(dir):
    """
    Turn in the direction opposite to the contact.
    """

    # We want to turn the robot wheels in opposite directions
    rightMotor.run_timed(speed_sp=dir * -750, time_sp=250)
    leftMotor.run_timed(speed_sp=dir * 750, time_sp=250)

    # Wait until both motors are stopped:
    while any(m.state for m in (leftMotor, rightMotor)):
        sleep(0.1)


def drive(left, right):
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def lost():
    # If robot cannot find object drive forward till boundary then do another check

    # Below loop, keeps the robot driving back and forth till target is found.
    while cs.value() > 30:
        drive(200, 200)
    # Didn't know the code, to make it spin 180 degrees.


while not btn.any():
    cs.mode = 'COL-REFLECT'
    # Didn't know the code, to make it spin 180 degrees.
    if us.value > 750:
        lost()
    elif us.value < 750 and cs.value() > 30:
        drive(200, 200)
