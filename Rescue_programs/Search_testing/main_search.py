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
rightMotor = LargeMotor(OUTPUT_A)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D)
assert leftMotor.connected
servo = Motor(OUTPUT_C)
assert servo.connected

print()
print("Motors Connected")
print()

# Connect sensors
sleep(0.5)
us = UltrasonicSensor(INPUT_1)
assert us.connected
us_front = UltrasonicSensor(INPUT_2)
assert us_front.connected
print("Ultrasonics Connected")
print()
cs = ColorSensor(INPUT_4)
assert cs.connected
print("Colour sensor connected")
print()
gs = GyroSensor(INPUT_3)
assert gs.connected
print("Gyro sensor connected")
print()
# Checking EV3 buttons state
btn = Button()

# ---GLOBAL IMPORTANT SETTINGS--- #
ultrasonic_wall_sensing_distance = 100
front_wall_sensing_distance = 10
scan_rotation_speed = 150
wheel_rotations_per_block = 818


# ---MOVEMENT FUNCTIONS--- #
#
# this function moves the bot forward or backwards 1 block
def move_1_block(forward):
    spins = wheel_rotations_per_block
    if forward:
        spins = spins * -1

    leftMotor.run_to_rel_pos(position_sp=spins, speed_sp=150, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=spins, speed_sp=150, ramp_down_sp=90)

    left_running_state = leftMotor.state
    right_running_state = rightMotor.state
    print("returning the state flags of the motor ", left_running_state, right_running_state)

    # wait until motor stops before continuing with anything else
    print("returning the state flags of the motor ", leftMotor.state, rightMotor.state)
    while leftMotor.state == left_running_state and rightMotor.state == right_running_state:
        if us.value() < ultrasonic_wall_sensing_distance:
            stop_motors()
            print("Wall was sensed early so motor stopped")


def move_1_block_2(forward):
    # TODO: Figure out how to do desired direction
    desired_direction = gs.value()
    print("The desired direction:", desired_direction)

    leftMotor.run_direct(duty_cycle_sp=75)
    rightMotor.run_direct(duty_cycle_sp=75)

    left_running_state = leftMotor.state
    right_running_state = rightMotor.state
    i = 0
    while i < 40:
        print("while loop count:", i)

        if us_front.value() < front_wall_sensing_distance:
            stop_motors()
            print()
            print("wall was sensed early so motor stopped")
            break
        elif gs.value() < desired_direction - 3:
            leftMotor.run_direct(duty_cycle=30)
            rightMotor.run_direct(duty_cycle=75)
            i += 1
        elif gs.value() > desired_direction + 3:
            leftMotor.run_direct(duty_cycle=75)
            rightMotor.run_direct(duty_cycle=30)
            i += 1
        else:
            leftMotor.run_direct(duty_cycle_sp=75)
            rightMotor.run_direct(duty_cycle_sp=75)
            i += 1
    stop_motors()

# this function stops both motors
def stop_motors():
    # leftMotor.reset()
    leftMotor.stop()
    # rightMotor.reset()
    rightMotor.stop()


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

    print()
    print("Lookin forward")
    # forward
    ultrasonic_movement(FRONT)
    sleep(5)
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


def main_program(past_moves, steps):
    """
    WRITE THE DAMN DOCSTRING
    :param past_moves:
    :param steps:
    :return:
    """
    while not btn.any():  # This should eventually be replaced with a colour sensor reading
        print()
        print("Bout to scan walls")
        scan_walls()
        if node_info[steps][0] or node_info[steps][1] or node_info[steps][2]:
            print()
            print("Looks like there's somewhere to go")
            decision_program(steps)
        else:
            print()
            print("Time to back the fuck up")
            backup_program(past_moves, steps)


def decision_program(steps):
    """

    :param steps: How many steps forward we have taken or the current reference index to past_moves

    :var : Each value appended to the list refers to a (movement)/(type of movement), as described below:
             0 = Forward movement
             1 = Right turn
             2 = Left turn
             NB: Does not require a reverse unit, as every time it reverses it will delete the preceding block

    :return: NO RETURN
    """

    if node_info[steps][0]:
        print()
        print("Let's go forward")
        move_1_block_2(True)
        stop_motors()
        past_moves.append(0)
        steps += 1
        main_program(past_moves, steps)
    else:
        print()
        print("Let's not go forward")
        if node_info[steps][1]:
            turn(1)
            past_moves.append(1)
            steps += 1
            move_1_block_2(True)
            stop_motors()
            past_moves.append(0)
            node_info.append(0)
            steps += 1
            main_program(past_moves, steps)
        elif node_info[steps][2]:
            turn(-1)
            past_moves.append(2)
            node_info.append(0)
            steps += 1
            move_1_block_2(True)
            stop_motors()
            past_moves.append(0)
            steps += 1
            main_program(past_moves, steps)


def backup_program(past_moves, steps):
    """

    :return:
    """
    last_entry = -1
    while node_info[steps][0] == False and node_info[steps][1] == False and node_info[steps][2] == False:
        if past_moves[steps] == 0:
            reverse()
            stop_motors()
            past_moves = past_moves[: -1]
            steps -= 1
            node_info[steps][1] = False
        elif past_moves[steps] == 1:
            turn(-1)
            past_moves = past_moves[: -1]
            steps -= 1
            node_info[steps][1] = False
        elif past_moves[steps] == 2:
            turn(1)
            past_moves = past_moves[: -1]
            steps -= 1
            node_info[last_entry][2] = False


past_moves = []  # Holds the information on how to get back to the beginning or back up to the last junction
node_info = [[True, False, False]]  # Holds the boolean values of the walls in each node, as we come across them
steps = 0  # This is our current step count

main_program(past_moves, steps)
