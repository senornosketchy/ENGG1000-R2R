#!/usr/bin/python3

# Lyalls Code to be Tested, 6th April, 2018.

# Functions
''' The robot should stop when the U/S is
'''


from time import sleep
import sys, os
from ev3dev.ev3 import *

# Connect Motors
rightMotor = Motor(OUTPUT_A)
assert rightMotor.connected
leftMotor = Motor(OUTPUT_D)
assert leftMotor.connected
print("Motors connected")
gs  = GyroSensor()
assert gs.connected
print("Gyro connected")
gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'	# Set gyro mode to return compass angle
sleep(0.2) #why is the sleep here

# Checking EV3 buttons state
btn = Button()

def drive(left, right):
    # Move left and right motors at the given speeds. Speeds depend
    # on the values of touch sensor, and ultrasonic.
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)

def stop():
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')



#main command line area
#rotations = 2.27
#leftMotor.on_for_rotations(speed_pct=50 , rotations=2.27, brake=False, block=True)
#rightMotor.on_for_rotations(speed_pct=80, rotations=2.27, brake=True, block=True)
leftMotor.run_to_abs_pos(position_sp=818, stop_command ='brake')
rightMotor.run_to_abs_pos(position_sp=818, stop_command='brake')

sleep(10)



stop()
