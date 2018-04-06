#!/usr/bin/python3

# sleep(2)

# Import the ev3dev specific library
from time import sleep
from ev3dev.ev3 import *


print("FUCKING PRINT")
print("1")
# Connect motors
rightMotor = LargeMotor(OUTPUT_C)

assert rightMotor.connected

leftMotor = LargeMotor(OUTPUT_B)
assert leftMotor.connected

# Connect sensors
print("2")
us = UltrasonicSensor(INPUT_1)

cs = ColorSensor(INPUT_4)

tsRIGHT = TouchSensor(INPUT_3)
tsLEFT = TouchSensor(INPUT_2)


# Declaring buttons
btn = Button()


# Basic movement control
def drive(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)

    rightMotor.run_direct(duty_cycle_sp=right)


# Spinning the robot, clockwise/anticlockwise depending on required direction
def search(spinDirection):
    drive(spinDirection * -100, spinDirection * 100)


# Stop both motors
def stop():
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


# Basic Start sequence
def start_sequence(spinDirection):
    # sleep(3)
    Sound.speak('WAAAALLL E')
    



# If the robot cannot see the other bot after the starting sequence
def lost():
    # If robot cannot find object drive forward to boundary then do another check
    # Below loop, keeps the robot driving back and forth till target is found.
    while us.value > 750 or not tsLEFT.value() or not tsRIGHT.value():
        while cs.value() > 30:
            drive(-80, -80)
        search(1)
    # Didn't know the code, to make it spin 180 degrees.


print("3")
while not btn.any():
    cs.mode = 'COL-REFLECT'
    start_sequence(1)
    lost()
    
    #if btn.left():
    #    start_sequence(1)
    #if btn.right():
    #    start_sequence(-1)
print("4")

# sleep(3)
