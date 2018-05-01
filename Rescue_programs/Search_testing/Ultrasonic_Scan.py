#!/usr/bin/python3

from time import sleep
import sys, os
from ev3dev.ev3 import *

# connect motors
rightMotor = LargeMotor(OUTPUT_A)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D)
assert leftMotor.connected

print("Motors connected")

# connect gyro
gs = GyroSensor()
assert gs.connected
print("Gyro connected")
gs.mode = 'GYRO-RATE'  # Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'

# connect servo
servo = Motor(OUTPUT_C)
assert servo.connected
servo.reset()
servo.stop()

print("Servo connected")

# connect ultrasonic
us = UltrasonicSensor()
assert us.connected

print("Ultrasonic Connected")

# all connected
Sound.speak('Get Ready... Go!').wait()
print("Everything connected")


# DEFINE GLOBAL VARIABLES


# FUNCTION DECLARATIONS

def scan(destination):
    servo.run_to_abs_pos(position_sp=destination, speed_sp=75, ramp_down_sp=90)


"""
    the main loop of this program will
        move forward a certain distance
        scan in 3 directions
        store each direction results
        print out scan results
"""


def scan_walls(input):
    global node_info

    # Declaring constants
    DETECTION_DISTANCE = 60
    FRONT = 0
    RIGHT = 90
    LEFT = -90

    # forward
    scan(FRONT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        forward = False
    else:
        forward = True

    # left
    scan(LEFT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        left = False
    else:
        left = True

    # right
    scan(RIGHT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        right = False
    else:
        right = True

    node_info.append((forward, right, left))


def main():
    # Left Center Right Array
    LCR = [0, 0, 0]

    while True:
        drive_square()
        # It will return to the main area while the robot moves
        scan(0)
        sleep(5)
        # set array front value
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
        # reset array
        LCR = [0, 0, 0]

        print("It has slept for 5 seconds")


main()
