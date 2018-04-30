#!/usr/bin/python3

from time import sleep
import sys, os
from ev3dev.ev3 import *

#connect motors
rightMotor = LargeMotor(OUTPUT_A)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D)
assert leftMotor.connected

print("Motors connected")

#connect gyro
gs  = GyroSensor()
assert gs.connected
print("Gyro connected")
gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'

#connect servo
servo = Motor(OUTPUT_C)
assert servo.connected
servo.reset()
servo.stop()

print("Servo connected")

#connect ultrasonic
us = UltrasonicSensor()
assert us.connected

print("Ultrasonic Connected")

#all connected
Sound.speak('Get Ready... Go!').wait()
print("Everything connected")

#DEFINE GLOBAL VARIABLES


#FUNCTION DECLARATIONS

def stop():
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')

def drive_square():
    #drive only a certain time
    rightMotor.run_timed(time_sp=3000, speed_sp=100)
    leftMotor.run_timed(time_sp=3000, speed_sp=100)
    print("moving forward 1 square")

#def turn(clockwise):

def scan(destination):
    servo.run_to_abs_pos(position_sp=destination, speed_sp=75, ramp_down_sp=90)
    #print("destination angle ", destination)

'''
    the main loop of this program will
        move forward a certain distance
        scan in 3 directions
        store each direction results
        print out scan results
'''

def print_array(input):
    detection_distance = 60

    output_string = ""

    #left
    if input[0] <= detection_distance:
        output_string += "left clear"
    else:
        output_string += "left blocked"
    output_string += str(input[0])

    #center
    if input[1] <= detection_distance:
        output_string += " center clear"
    else:
        output_string += " center blocked"
    output_string += str(input[1])

    #right
    if input[2] <= detection_distance:
        output_string += " right clear"
    else:
        output_string += " right blocked"
    output_string += str(input[2])

    print(output_string)



def main():
    # Left Center Right Array
    LCR = [0,0,0]

    while True:
        drive_square()
        # It will return to the main area while the robot moves
        scan(0)
        sleep(5)
        #set array front value
        LCR[1] = us.value()


        scan(90)
        sleep(5)
        # set array left value
        LCR[0] = us.value()

        scan(-90)
        sleep(5)
        # set array front value
        LCR[2] = us.value()

        print_array(LCR)
        #reset array
        LCR = [0,0,0]

        print("It has slept for 5 seconds")



main()
