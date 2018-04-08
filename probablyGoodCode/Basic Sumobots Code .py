#!/usr/bin/python3

# This program is the basic form of the sumobot program
# 1. Connect sensors and initialise motors
# 2. Wait 3 seconds before starting

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

def start()
    #delay
    sleep(3);
    #scan for the robot by spinning CLOCKWISE for 90 DEGREES
    direction = gs.value();
    
    while (direction < 90):
        rightMotor.run_direct(duty_cycle_sp = -75)
        leftMotor.run_direct(duty_cycle_sp = 75)
        direction = gs.value();

start()
while not btn.any():
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
rightMotor.stop()
leftMotor.stop()
