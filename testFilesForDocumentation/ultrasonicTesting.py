#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

us = UltrasonicSensor(INPUT_2)
assert us.connected

btn = Button()

def ultrasonic_movement(destination):
    servo.run_to_abs_pos(position_sp=destination, speed_sp=75, ramp_down_sp=90)


def scan_walls():
    global node_info

    # Declaring constants
    DETECTION_DISTANCE = 100
    FRONT = 0
    RIGHT = 90
    LEFT = -90

    print()
    print("Lookin forward")
    # forward
    ultrasonic_movement(FRONT)
    sleep(5)
    print("The ultrasonic value is:", us.value())
    if us.value() <= DETECTION_DISTANCE:
        forward = False
        print("Not goin that way")
    else:
        forward = True
        print("Forwards clear")

    print()
    print("Lookin to the side")
    # left
    ultrasonic_movement(LEFT)
    sleep(5)
    print("The ultrasonic value is:", us.value())
    if us.value() <= DETECTION_DISTANCE:
        left = False
        print("Not goin left")
    else:
        left = True
        print("Left is clear")

    # right
    print()
    print("Lookin the other side")
    ultrasonic_movement(RIGHT)
    sleep(5)
    print("The ultrasonic value is:", us.value())
    if us.value() <= DETECTION_DISTANCE:
        right = False
        print("Right is blocked")
    else:
        right = True
        print("Right's clear")

    print()
    print("This is what we know")
    print((forward, left, right))
    node_info.append((forward, right, left))
    sleep(5)

while not btn.any():
    sleep(0.1)
    print(us.value(), "mm")
