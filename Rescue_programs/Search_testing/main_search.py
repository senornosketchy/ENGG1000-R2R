#!/usr/bin/python3
"""
Tanvee Islam, 29th April, 2018

SEARCHING PROGRAM

    Aim: The aim of this program is to successfully navigate a maze until a payload hidden inside the maze is identified

"""

# Importing necessary libraries
from time import sleep
import sys, os
from ev3dev.ev3 import *


# CONNECTING SENSORS AND MOTORS

# Connecting Motors
rightMotor = LargeMotor(OUTPUT_C)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected
servo = ServoMotor()
assert ServoMotor.connected

print("Motors Connected")
print()
print()


# TODO: Correct the sensors to what we are using
# Connect sensors
sleep(0.2)
us = UltrasonicSensor()
assert us.connected
print("Ultrasonic Connected")
print()
cs = ColourSensor(INPUT_4)
assert cs.connected
print("Colour sensor connected")
print()
gs = GyroSensor()
assert gs.connected
print("Colour sensor connected")
print()
# Checking EV3 buttons state
btn = Button()


def forward():
    """
    Write the damn docstring
    :return:
    """
    # Move left and right motors at the given speeds. Speeds depend
    # on the values of touch sensor, and ultrasonic.
    rightMotor.run_timed(time_sp=3000, speed_sp=100)
    leftMotor.run_timed(time_sp=3000, speed_sp=100)


def reverse():
    """
    Write the damn docstring
    :return:
    """
    leftMotor.run_timed(time_sp=1000, speed_sp=-500)
    rightMotor.run_timed(time_sp=1000, speed_sp=-500)


def turn(direction):
    """
    AIM: TO TURN THE ROBOT 90 DEGREES CLOCKWISE OR COUNTERCLOCKWISE 90 DEGREES

    :param direction: Either a 1 for right turns or -1 for left turns

    :return: NO RETURN
    """

    # TODO: Experiment to find the right speed and time values to turn 90 degrees
    leftMotor.run_timed(time_sp=1000, speed_sp=direction*500)
    rightMotor.run_timed(time_sp=1000, speed_sp=direction*(-500))


def stop():
    """
    Prolly don't even need this tbh
    :return:
    """
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


def ultrasonic_movement(destination):
    servo.run_to_abs_pos(position_sp=destination, speed_sp=75, ramp_down_sp=90)


def scan_walls():
    global node_info

    # Declaring constants
    DETECTION_DISTANCE = 60
    FRONT = 0
    RIGHT = 90
    LEFT = -90

    # forward
    ultrasonic_movement(FRONT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        forward = False
    else:
        forward = True

    # left
    ultrasonic_movement(LEFT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        left = False
    else:
        left = True

    # right
    ultrasonic_movement(RIGHT)
    sleep(5)
    if us.value <= DETECTION_DISTANCE:
        right = False
    else:
        right = True

    node_info.append((forward, right, left))


def main_program(past_moves, steps):
    """
    WRITE THE DAMN DOCSTRING
    :param past_moves:
    :param steps:
    :return:
    """
    while not btn.any():  # This should eventually be replaced with a colour sensor reading
        scan_walls()
        if node_info[steps][0] or node_info[steps][1] or node_info[steps][2]:
            decision_program(steps)
        else:
            backup_program(past_moves, steps)


def decision_program(steps):
    """

    :param steps: How many steps forward we have taken or the current reference index to past_moves

    :var past_moves: Each value appended to the list refers to a (movement)/(type of movement), as described below:
             0 = Forward movement
             1 = Right turn
             2 = Left turn
             NB: Does not require a reverse unit, as every time it reverses it will delete the preceding block

    :return: NO RETURN
    """

    if node_info[steps][0]:
        forward()
        past_moves.append(0)
        steps += 1
        main_program(past_moves, steps)
    else:
        if node_info[steps][1]:
            turn(1)
            past_moves.append(1)
            steps += 1
            forward()
            past_moves.append(0)
            node_info.append(0)
            steps += 1
            main_program(past_moves, steps)
        elif node_info[steps][2]:
            turn(-1)
            past_moves.append(2)
            node_info.append(0)
            steps += 1
            # confirm() ADD A CONFIRMATION THING MAYBE?, prolly not aye
            forward()
            past_moves.append(0)
            steps += 1
            main_program(past_moves, steps)


def backup_program(past_moves, steps):
    # TODO: WRITE THE PROGRAM and docstring
    """

    :return:
    """
    last_entry = -1
    while node_info[steps][0] == False and node_info[steps][1] == False and node_info[steps][2] == False:
        if past_moves[steps] == 0:
            reverse()
            past_moves = past_moves[: -1]
            steps -= 1

        elif past_moves[steps] == 1:
            turn(-1)
            past_moves = past_moves[: -1]
            steps -= 1
            node_info[steps][1] = False
        elif past_moves[steps] == 2:
            turn(1)
            past_moves = past_moves[:-1]
            steps -= 1
            node_info[last_entry][2] = False


def confirm():
    """
    AIM: To confirm that there is not a wall in the direction we are moving before recursively calling main_program
    :return: NO RETURN
    """


past_moves = []  # Holds the information on how to get back to the beginning or back up to the last junction
node_info = [[True, False, False]]  # Holds the boolean values of the walls in each node, as we come across them
steps = 0  # This is our current step count
