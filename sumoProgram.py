#!/usr/bin/python3

# Anshul Arora, Tanvee Islam, 6th April, 2018.


from time import sleep
import sys, os
from ev3dev.ev3 import *

# Connect Motors
rightMotor = LargeMotor(OUTPUT_C)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected
print("Motors connected")
sleep(0.2)

# Connect sensors
tsLeft = TouchSensor(INPUT_2)
assert tsLeft.connected
tsRight = TouchSensor(INPUT_3)
assert tsRight.connected
print("Touch sensors connected")
sleep(0.2)
us = UltrasonicSensor()
assert us.connected
print("Ultrasonic Connected")
cs = ColorSensor(INPUT_4)
assert cs.connected
print("Colour sensor connected")
# Checking EV3 buttons state
btn = Button()


def drive(left, right):
    # Move left and right motors at the given speeds. Speeds depend
    # on the values of touch sensor, and ultrasonic.
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def search(spinDirection):
    # Spin to detect other robot.
    drive(spinDirection * -100, spinDirection * 100)


def stop():
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


def mainprogram(direction):
    while True:  # while no button is pressing pressed do the following
        sleep(3)
        cs.mode = 'COL-REFLECT'
        search(direction)
        if us.value() < 500:
            drive(100, 100)
        elif tsRight.value() and tsLeft.value():
            drive(100, 100)
        elif tsLeft.value() and not tsRight.value():
            drive(100, 80)
            sleep(0.2)
        elif tsRight.value() and not tsLeft.value():
            drive(80, 100)
            sleep(0.2)
        elif cs.value() < 30:
            drive(100, 100)
            sleep(0.1)
        elif btn.backspace:
            break
        else:
            search(direction)
    stop()


sleep(0.5)
print("sumoProgram loaded, waiting for command")
sleep(0.2)
print("Left for anticlockwise, Right for clockwise")
while True:
    if btn.left:
        mainprogram(1)
    elif btn.right:
        mainprogram(-1)
    elif btn.backspace:
        break
stop()
