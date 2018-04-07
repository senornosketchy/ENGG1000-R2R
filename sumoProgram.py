#!/usr/bin/python3

# Anshul Arora, 6th April, 2018.


from time import sleep
import sys, os
from ev3dev.ev3 import *

# Connect Motors
rightMotor = LargeMotor(OUTPUT_C)
leftMotor = LargeMotor(OUTPUT_B)

# Connect sensors
tsLeft = TouchSensor(INPUT_2)
assert tsLeft.connected
tsRight = TouchSensor(INPUT_3)
assert tsRight.connected
us = UltrasonicSensor()
assert us.connected
cs = ColorSensor(INPUT_4)
assert cs.connected

# Checking EV3 buttons state
btn = Button()


def drive(left, right):
    # Move left and right motors at the given speeds. Speeds depend
    # on the values of touch sensor, and ultrasonic.
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def search(spinDirection):
    # Spin to detect other robot.
    drive(spinDirection * -50, spinDirection * 50)


def stop():
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


def mainProgram(direction)
    while True:  # while no button is pressing pressed do the following
        sleep(3)
        cs.mode = 'COL-REFLECT'
        if tsRight.value() and tsLeft.value():
            drive(100, 100)
        elif us.value() < 40:
            drive(100, 100)
        elif tsLeft.value() and not tsRight.value():
            drive(80, 50)
        elif tsRight.value() and not tsLeft.value():
            drive(50, 80)
        elif us.value < 750 and cs.value() > 40:
            drive(50, 50)
        elif btn.backspace:
            break
        else:
            search(direction)
    stop()

print("Push left to go anti, right to go clockwise")
while True:
    if btn.left:
        mainProgram(1)
    elif btn.right:
        mainProgram(-1)



