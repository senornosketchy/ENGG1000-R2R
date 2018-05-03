#!/usr/bin/python3

from time import sleep
import sys, os
from ev3dev.ev3 import *

# Connect Motors
rightMotor = Motor(OUTPUT_A)
assert rightMotor.connected
leftMotor = Motor(OUTPUT_D)
assert leftMotor.connected
print("Motors connected")

# SETUP COLOUR SENSOR
cs = ColorSensor(INPUT_3)
cs.mode = 'RGB-RAW'
assert cs.connected
print("color sensor")

# connect ultrasonic
us = UltrasonicSensor(INPUT_1)
assert us.connected

us_front = UltrasonicSensor(INPUT_2)
assert us_front.connected
print("Ultrasonic Connected")

def beeping_flashing():
    Sound.tone([(1000, 500, 500)] * 5)

    while 1:
        Leds.set_color(Leds.RIGHT, Leds.RED)
        Leds.set_color(Leds.LEFT, Leds.RED)
        time.sleep(1)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        time.sleep(1)

def main():
    sensing = True
    colour = 0
    found = False

    leftMotor.reset()
    leftMotor.stop()

    rightMotor.reset()
    rightMotor.stop()

    while not found:

        leftMotor.run_to_abs_pos(position_sp=-818, speed_sp=150, ramp_down_sp=90)
        rightMotor.run_to_abs_pos(position_sp=-818, speed_sp=150, ramp_down_sp=90)

        if us_front.value() < 10:
            found = True

    while sensing:
        print(colour)

        difference = us.value() - us_front.value()
        sleep(0.1)
        difference2 = us.value() - us_front.value()
        sleep(0.1)
        difference3 = us.value() - us_front.value()
        colour = cs.red

        if (difference > 125 and difference2 > 125 and difference3 > 125) and colour >= 3:
            beeping_flashing()
        print("Difference ", difference)

        sleep(1)






main()
