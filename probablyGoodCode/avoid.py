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

#Connect motors
rightMotor = LargeMotor(OUTPUT_B)
leftMotor  = LargeMotor(OUTPUT_C)

# Connect touch sensors.
ts1 = TouchSensor(INPUT_1);	assert ts1.connected
ts4 = TouchSensor(INPUT_4);	assert ts4.connected
us  = UltrasonicSensor();	assert us.connected
gs  = GyroSensor();		assert gs.connected

gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'	# Set gyro mode to return compass angle

# We will need to check EV3 buttons state.
btn = Button()

def start():
	"""
	Start both motors. `run-direct` command will allow to vary motor
	performance on the fly by adjusting `speed_sp` attribute.
	"""
	rightMotor.run_direct(duty_cycle_sp = 75)
	leftMotor.run_direct(duty_cycle_sp = 75)

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
	rightMotor.run_timed(speed_sp=dir*-750, time_sp=250)
	leftMotor.run_timed(speed_sp=dir*750, time_sp=250)

	# Wait until both motors are stopped:
	while any(m.state for m in (leftMotor, rightMotor)):
		sleep(0.1)

# Run the robot until a button is pressed.
start()
while not btn.any():

	# If we bump an obstacle, back away, turn and go in other direction.

	if ts1.value():
		backup()
		turn(1)
		start()

	if ts4.value():
		backup()
		turn(-1)
		start()

	# Keep the robot going in the same direction

	direction = gs.value();
	# print direction

	if direction > 5:
		# print('right')
		rightMotor.duty_cycle_sp = 5
	elif direction < -5:
		# print('left')
		leftMotor.duty_cycle_sp = 5
	else:
		leftMotor.duty_cycle_sp = 75
		rightMotor.duty_cycle_sp = 75

	# Ultrasonic sensor will measure distance
	# to the closest object in front of it.
	distance = us.value();

	if distance > 300:
		# Path is clear, run at full speed.
		dc = 75
	else:
		# Obstacle ahead, slow down.
		dc = 30

	for m in (leftMotor, rightMotor):
		m.duty_cycle_sp = dc

	print(rightMotor.position, leftMotor.position)

# Stop the motors before exiting.
rightMotor.stop()
leftMotor.stop()
