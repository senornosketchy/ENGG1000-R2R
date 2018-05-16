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

print("\nMotors Connected\n")

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

def can_pick_up():
