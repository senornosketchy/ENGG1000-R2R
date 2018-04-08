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
    drive(spinDirection * -50, spinDirection * 50)


# Stop both motors
def stop():
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


# Basic Start sequence
def start_sequence(spinDirection):
    # sleep(3)
    Sound.speak('WAAAALLL E')
    while not btn.any():
        if us.value() < 500:
            drive(100, 100)
        else:
            search(1)



# If the robot cannot see the other bot after the starting sequence
def lost():
    # If robot cannot find object drive forward to boundary then do another check
    # Below loop, keeps the robot driving back and forth till target is found.
    while us.value > 750 and not tsLEFT.value() and not tsRIGHT.value():
        while cs.value() > 30:
            drive(-20, -20)
        search(1)
    # Didn't know the code, to make it spin 180 degrees.

drive(20,20)
print("3")
while not btn.any():
    cs.mode = 'COL-REFLECT'
    start_sequence(1)
    lost()
    if (tsRIGHT.value() and tsLEFT.value) or us.value() < 40():
        drive(100, 100)
    elif us.value() < 400 and cs.value() > 40:
        drive(70, 70)
    elif tsLEFT.value() and not tsRIGHT.value():
        drive(80, 50)
    elif tsRIGHT.value() and not tsLEFT.value():
        drive(50, 80)

    else:
        continue

    #if btn.left():
    #    start_sequence(1)
    #if btn.right():
    #    start_sequence(-1)
print("4")

# sleep(3)
