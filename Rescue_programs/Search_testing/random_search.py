#!/usr/bin/python3

# Anshul Arora, Tanvee Islam, 6th April, 2018.


from time import sleep
import sys, os
from ev3dev.ev3 import *

class Node:

    def __init__(self, id, neighbours):
        self.id = id
        self.neighbours = neighbours
        self.visited = False

# Connect Motors
rightMotor = LargeMotor(OUTPUT_C)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected
Sound.speak("Motors connected")
sleep(0.2)

# Connect sensors
tsLeft = TouchSensor(INPUT_2)
assert tsLeft.connected
tsRight = TouchSensor(INPUT_3)
assert tsRight.connected
Sound.speak("Touch sensors connected")
sleep(0.2)
us = UltrasonicSensor()
assert us.connected
Sound.speak("Ultrasonic Connected")
gs = GyroSensor(INPUT_4)
assert gs.connected
Sound.speak("Colour sensor connected")
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


def dfs_open_list(start):
    open_list = [start]
    while open_list != []:
        first, rest = open_list[0], open_list[1:]
        if first.visited == True:
            open_list = rest
        else:
            print('Node ', first.id)
            first.visited = True
            open_list = first.neighbours + rest


sleep(0.5)
print("sumoProgram loaded, waiting for command:")
sleep(0.5)
print("Left for anticlockwise, Right for clockwise")
while True:
    if btn.left:
        sleep(3)
        Sound.speak('You will now be destroyed')
        mainprogram(1)
    elif btn.right:
        sleep(3)
        Sound.speak('You will now be destroyed')
        mainprogram(-1)
    elif btn.backspace:
        break
stop()
