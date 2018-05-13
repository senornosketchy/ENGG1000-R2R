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


wheel_turn_rotations_per_turn = 360 * 0.89 * 2

def stop_motors():
    # leftMotor.reset()
    leftMotor.stop()
    # rightMotor.reset()
    rightMotor.stop()


def turn(left):
    # increments setting for the turn
    direction = 1
    if left:
        direction = -1

    # MAJOR TURN
    leftMotor.run_to_rel_pos(position_sp=wheel_turn_rotations_per_turn * direction, speed_sp=200, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=-wheel_turn_rotations_per_turn * direction, speed_sp=200, ramp_down_sp=90)

    # hold until the motor starts
    leftMotor.wait_while('running')

    stop_motors()


turn(False)
