#!/usr/bin/python

"""
EV3 program to drive one direction but try to go around obstacles when bumped.
Author: Claude Sammut
Date: 1 April 2016

This is a cleaned up version of "avoid.py". It's a simple program but has one drawback.
When the program sleeps to allow timing on the backup and turn, the robot can't listen
to it's sensors, so if there is another contact, it can't restart the backup until the
first call is finished.
"""

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# Import the ev3dev specific library
from ev3dev.ev3 import *

#Connect motors
rightMotor = LargeMotor(OUTPUT_B)
leftMotor  = LargeMotor(OUTPUT_C)

# Connect touch sensors.
ts1 = TouchSensor(INPUT_1);	assert ts1.connected
ts4 = TouchSensor(INPUT_4);	assert ts4.connected
us  = UltrasonicSensor();	assert us.connected
gs  = GyroSensor();		assert gs.connected

# The gyro is reset when the mode is changed, so the first line is extra, just so we
# can change the mode the 'GYRO-ANGLE', which is what we want
gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'	# Set gyro mode to return compass angle

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

def backup(dir):
	"""
	Back away from an obstacle and
	turn in the direction opposite to the contact
	"""

	# Sound backup alarm.
	Sound.tone([(1000, 500, 500)] * 3)

	# Turn backup lights on:
	Leds.set_color(Leds.LEFT, Leds.RED)
	Leds.set_color(Leds.RIGHT, Leds.RED)

	# Stop both motors and reverse for 1.5 seconds
	start(-50, -50)
	sleep(1.5)

	# Turn the robot wheels in opposite directions for 0.25 seconds
	start(dir*75, -dir*75)
        sleep(0.25)

	# Turn backup lights off:
	Leds.set_color(Leds.LEFT, Leds.GREEN)
	Leds.set_color(Leds.RIGHT, Leds.GREEN)


# Run the robot until a button is pressed.

while not btn.any():
	"""
	If we bump an obstacle, back away, turn and go in other direction.
	We also check the gyro angle and try to keep the robot heading in
	the same direction that it started in.
	The default action is to go straight but the robot slows down if the
	ultrasonic sensor reports an obstacle ahead.
	"""
	if ts1.value():
                backup(-1)
	elif ts4.value():
                backup(1)
	elif gs.value() < -5:
		start(30, 75)
	elif gs.value() > 5:
		start(75, 30)
	else:
		dc = 75 if us.value() > 300 else 30
		start(dc, dc)

# Stop the motors before exiting.
stop()
