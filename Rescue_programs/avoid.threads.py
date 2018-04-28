#!/usr/bin/python


"""
EV3 program to drive one direction but try to go around obstacles when bumped.
Author: Claude Sammut
Date: 1 April 2016

This program gets around the limitation of 'avoid.tidy.py', which can't handle
a new contact during the backup.

We introduce Python's threading mechanism. This is more complicated than using
exceptions, like in 'avoid.except.py' but allows us to separate handling of the
sensors from the motor control and gives us more flexibility.

Threads allow several pieces of code to run concurrently. We will run the motors
in a new thread whenever a new action is required. Because the motors are being
controlled in their own thread, the main program can keep looping, checking the
sensors. If the sensors indicate that a new action is required, we interrupt the
motor thread, let it die, and start a new thread for the new action.

An action can consist of a sequence of motor commands, e.g. avoiding an obstacle
includes a backup and a turn. An action sequence is represented by a list of
tuples (left_motor_speed, right_motor_speed, duration).
"""

# Import a few system libraries that will be needed
from time import sleep
import sys, os
import threading

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

gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'	# Set gyro mode to return compass angle
btn = Button()		# We will need to check EV3 buttons state.

"""
The 'threading' library defines a class 'Thread'. This code extends a Thread to
handle the motor control.
"""

class RunMotors(threading.Thread):

	def __init__(self, action_list):
		"""
		__init__ is called when the thread object is created. It is executed once only
		to initialise the object's local variables
		"""
		threading.Thread.__init__(self)
		self.action_list = action_list
		self.interrupt = False
		left = right = 0

	def run(self):
		"""
		Run the motors for the specified duration but wake up every 0.1 seconds to
		check if the interrupt flag has been set. If so, return. As this is the only
		code that should be running in this thread, returning, should cause the thread
		to terminate.
		"""
		for (left, right, duration) in self.action_list:
			self.left = left
			self.right = right
			# Execute a sequence of actions
			leftMotor.run_direct(duty_cycle_sp=left)
			rightMotor.run_direct(duty_cycle_sp=right)

			while duration > 0:
				sleep(0.1)
				duration -= 0.1
				if self.interrupt:
					return

	def stop(self):
		"""
		A tidy way to set the interrupt flag inside this thread object
		"""
		self.interrupt = True

def stop():
	# Stop both motors
	leftMotor.stop(stop_action='brake')  
	rightMotor.stop(stop_action='brake')


def new_action(interrupt, action_list):
	"""
	if 'interrupt' is True, this will stop the current action befor starting
	the new one. In either case, 'join' causes the main thread to wait for the
	current motor thread to terminate before starting the new one.
	"""
	global current_action
	if interrupt:
		current_action.stop();
	current_action.join()
	current_action = RunMotors(action_list)
	current_action.start()
	
# Run the robot until a button is pressed.

current_action = RunMotors([(75, 75, 10)])
current_action.start()

while True:
	"""
	If we bump an obstacle, back away, turn and go in other direction.
	"""

	# This loop only terminates if a button on the EV3 is pressed
	if btn.any():
		current_action.stop()
		stop()
		sys.exit()
	# If the left touch sensor makes contact, stop the current motor thread
	# and start backin up. The action list tells the robot to reverse at
	# half speed for 1.5 seconds then turn right for 0.25 seconds
	elif ts1.value():
		new_action(True, [(-50, -50, 1.5), (-75, 75, 0.25)])
	# If the right touch sensor makes contact, stop the current motor thread
	# and start backin up. The action list tells the robot to reverse at
	# half speed for 1.5 seconds then turn left for 0.25 seconds
	elif ts4.value():
		new_action(True, [(-50, -50, 1.5), (75, -75, 0.25)])
	# If the ultrasonic sensor tells us that there is an obstacle ahead
	# and we are going straight ahead at 75% speed, slow down to 30%
	elif us.value() < 300 and current_action.left == 75:
		new_action(True, [(30, 30, 10)])
	# If the ultrasonic sensor tells us that there is no obstacle nearby
	# and we are going straight ahead at 30% speed, speed up to 75%
	elif us.value() >= 300 and current_action.left == 30:
		new_action(True, [(75, 75, 10)])
	# If we are moving forward (both motors positive speed) but the gyro tells
	# us the robot has difted left, change the speed of the motors to vere right
	elif current_action.left > 0 and current_action.right > 0 and gs.value() < -5:
		new_action(True, [(30, 75, 0.25)])
	# If we are moving forward (both motors positive speed) but the gyro tells
	# us the robot has difted right, change the speed of the motors to vere left
	elif current_action.left > 0 and current_action.right > 0 and gs.value() > 5:
		new_action(True, [(75, 30, 0.25)])
	# We only get here if the robot is in the clear and on course, so if the motors
	# turning at different speeds, we want to straighten up.
	elif current_action.left != current_action.right:
		new_action(False, [(75, 75, 10)])
