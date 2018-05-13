#!/usr/bin/python3

from ev3dev.ev3 import *
from time import sleep

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

btn = Button()

def turn(target_angle, direction):
    """
    AIM: TO TURN THE ROBOT 90 DEGREES CLOCKWISE OR COUNTERCLOCKWISE 90 DEGREES

    :param direction: Either a 1 for right turns or -1 for left turns

    :return: NO RETURN
    """
    init_angle = gs.value() % 180
    print("The inital angle:", init_angle)

    print("The initial difference is:", init_angle - target_angle)

    # TODO: Experiment to find the right speed and time values to turn 90 degrees
    while abs(init_angle - target_angle) < 95:
        print("The difference angle is now:", abs(init_angle - target_angle))

        leftMotor.run_direct(duty_cycle_sp=direction * 40)
        rightMotor.run_direct(duty_cycle_sp=direction * -40)
        init_angle = gs.value() % 180

    # while gs.value() % 360 != init_angle + direction*(target_angle - 1) or gs.value() % 360 != init_angle + \
    #         direction*target_angle or gs.value() % 360 != init_angle + direction*(target_angle + 1):
    #     print(gs.value() % 360)
    #     leftMotor.run_direct(duty_cycle_sp=direction*60)
    #     rightMotor.run_direct(duty_cycle_sp=direction*-60)
    print("The final angle is:", init_angle)


def stop_motors():
    # leftMotor.reset()
    leftMotor.stop()
    # rightMotor.reset()
    rightMotor.stop()


turn(90, 1)
stop_motors()

print()
print(gs.value() % 180)
