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
rightMotor.stop()
rightMotor.reset()
assert rightMotor.connected
leftMotor = Motor(OUTPUT_D)
leftMotor.stop()
leftMotor.reset()
assert leftMotor.connected
print("Motors connected")
gs = GyroSensor()
assert gs.connected
print("Gyro connected")
gs.mode = 'GYRO-RATE'  # Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'  # Set gyro mode to return compass angle
sleep(0.2)  # why is the sleep here



def gsturn(left):
    
    #SET DIR PREFIX AND RECORD FIRST ANGLE
    
    beginning_angle = gs.value()
    if left == True:
        #assuming that the right (clockwise) dir is positive
        direction_prefix = -1
    else:
        direction_prefix = 1
        
    
    #FIND NEAREST 90 IN THE DIRECTION OF TURN
    destination_angle = beginning_angle + (direction_prefix * 45)
    while destination_angle % 90 != 0:
        destination_angle += direction_prefix

    destination_angle = destination_angle + (-direction_prefix*4)
    print("Destination is ", destination_angle)



    #START DRIVING IN CORRECT DIR
    leftMotor.run_to_rel_pos( position_sp=  350 * direction_prefix, speed_sp=200, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp= -350 * direction_prefix, speed_sp=200, ramp_down_sp=90)

    run_state = leftMotor.state
    
    #LOOP TO BREAK ONCE THE GYRO IS IN CORRECT RANGE
    while (gs.value() < destination_angle - 1 and gs.value() < destination_angle + 1) or (gs.value() > destination_angle - 1 and gs.value() > destination_angle + 1):
        print(gs.value());
        if leftMotor.state != run_state:
            print("Motor was stopped by rel_pos")
            break

    #STOP MOTORS IMMEDIATELY    
    stop_motors()
    print("finishing gyroscopic turn")

def stop_motors():
    print("stop turning")
    #leftMotor.reset()
    leftMotor.stop()

    #rightMotor.reset()
    rightMotor.stop()


#should return to orig position
#L, R, R, L
gsturn(True)
sleep(.5)
print("The final value isL", gs.value())
gsturn(False);
sleep(.5)
print("The final value isL", gs.value())
gsturn(False);
sleep(.5)
print("The final value isL", gs.value())
sleep(3)
gsturn(True);
sleep(.5)
print("The final value isL", gs.value())
gsturn(True);
sleep(.5)
print("The final value isL", gs.value())
gsturn(True);
sleep(.5)
print("The final value isL", gs.value())
gsturn(True);
sleep(.5)
print("The final value isL", gs.value())
stop_motors()

