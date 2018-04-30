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

print("Motors Connected")
print()
print()


#TODO: Correct the sensors to what we are using
# Connect sensors
tsLeft = TouchSensor(INPUT_2)
assert tsLeft.connected
tsRight = TouchSensor(INPUT_3)
assert tsRight.connected
print("Touch sensors connected")
sleep(0.2)
us = UltrasonicSensor()
assert us.connected
Sound.speak("Ultrasonic Connected")
gs = GyroSensor(INPUT_4)
assert gs.connected
Sound.speak("Colour sensor connected")
# Checking EV3 buttons state
btn = Button()


def forward():
    # Move left and right motors at the given speeds. Speeds depend
    # on the values of touch sensor, and ultrasonic.
    #TODO: Adjust values to go forward one "block"
    leftMotor.run_timed(time_sp = 1000, speed_sp = 500)
    rightMotor.run_timed(time_sp = 1000, speed_sp = 500)


def turn(direction):
    """
    AIM: TO TURN THE ROBOT 90 DEGREES CLOCKWISE OR COUNTERCLOCKWISE 90 DEGREES

    :param direction: Either a 1 for right turns or -1 for left turns

    :return: NO RETURN
    """

    #TODO: Experiment to find the right speed and time values to turn 90 degrees
    leftMotor.run_timed(time_sp=1000, speed_sp=direction*500)
    rightMotor.run_timed(time_sp=1000, speed_sp=direction*(-500))


def stop():
    # Brake the motors of the robot.
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


def ultrasonic_movement():
    """
    Code will come from Lyall
    The aim of this function is to use the actuator/small motor to turn the ultrasonic at 90 degree intervals to detect
    whether or not there is a wall. Three boolean values for forward, left and right will be returned in a three-tuple
    to be used to determine which direction to go.

    forward: [Boolean]
    left: [Boolean]
    right: [Boolean

    :return: (forward, left, right)
    """

    # TODO: STEAL THE FUNCTION FROM LYALL
    forward = True
    right = False
    left = False

    return forward, right, left


def main_program(past_moves, steps):
    while not btn.any():  # This should eventually be replaced with a colour sensor reading
        if node_info[steps[0]] or node_info[steps[1]] or node_info[steps[2]]:
            decision_program(steps)
        else:
            backup_program(steps)


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

    if node_info[steps[0]]:
        forward()
        past_moves.append(0)
        steps += 1
        main_program(past_moves, steps)
    else:
        if node_info[steps[1]]:
            turn(1)
            past_moves.append(1)
            steps += 1
            confirm()
        elif node_info[steps[2]]:
            turn(-1)
            past_moves.append(2)
            steps += 1
            confirm()
        else:
            backup_program()

def backup_program():
    #TODO: WRITE THE PROGRAM


def confirm():
    """
    AIM: To confirm that there is not a wall in the direction we are moving before recursively calling main_program
    :return: NO RETURN
    """
    


past_moves = []  # Holds the information on how to get back to the beginning or back up to the last junction
node_info = [(True, False, False)]  # Holds the boolean values of the walls in each node, as we come across them
steps = 0  # This is our current step count
