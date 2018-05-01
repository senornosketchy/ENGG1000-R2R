#!/usr/bin/python3

from time import sleep
import sys, os
from ev3dev.ev3 import *

#---SENSOR INITIALISATION---#
#
# announce it
print("#---INITIALISING---#\n")

# connect motors
rightMotor = LargeMotor(OUTPUT_A)
assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D)
assert leftMotor.connected
print("Motors connected")

# connect gyro
gs = GyroSensor()
assert gs.connected
print("Gyro connected")


# connect servo
servo = Motor(OUTPUT_C)
assert servo.connected
print("Servo connected")

# connect ultrasonic
us = UltrasonicSensor()
assert us.connected
print("Ultrasonic Connected")

# connect color
cs = ColorSensor(INPUT_3)
assert cs.connected
print("Color Connected")

# 1. all connected
Sound.speak('Get Ready... Go!').wait()
print("*100% SUCCESSFUL*")

# 2. calibrate and test here
cs.mode = 'COL-REFLECT'     # color
gs.mode = 'GYRO-RATE'       # gyro: changing the mode resets the gyro
gs.mode = 'GYRO-ANG'
leftMotor.reset()           # motors
rightMotor.reset()
servo.reset()               # servo
servo.stop()


#---GLOBAL IMPORTANT SETTINGS---#
ultrasonic_wall_sensing_distance = 100
scan_rotation_speed = 150
wheel_rotations_per_block = 818




#---1. SCANNING FUNCTIONS---#
#
# this function controls all the scanning sub-functions
def start_scan():
    # initialise array to hold ultrasonic data raw
    LCR_raw = [ 0, 0, 0 ]

    # Center reading
    can_check()
    LCR_raw[1] = us.value()

    # Left
    rotate_sensors(-90, scan_rotation_speed)
    can_check()
    LCR_raw[0] = us.value()

    # Right
    rotate_sensors(90, scan_rotation_speed)
    can_check()
    LCR_raw[2] = us.value()

    # return to the center
    rotate_sensors(0, 125)

    # format the LCR_bool array
    LCR_clear_bool = are_routes_clear(LCR_raw)

    #return a boolean array based on whether directions are clear
    return LCR_clear_bool

# this function rotates the sensors at a certain speed to a relative point
def rotate_sensors(destination, speed):
    print("rotating sensors to: ", destination)
    servo.run_to_abs_pos(position_sp=destination, speed_sp=speed, ramp_down_sp=90)
    sleep(5)

# this function checks the value of the colour sensor to see if it has sensed the can
def can_check():
    reading1 = cs.red
    sleep(1)
    reading2 = cs.red
    print("colour values: ", reading1, reading2)

    # if both values were red, start flashing
    if reading1 > 3 and reading2 > 3:
        beeping_flashing()

# this function determines whether the routes are clear based on ultrasonic data
def are_routes_clear(LCR_raw):
    print("Raw data: ", LCR_raw)

    LCR_clear_bool = [ 0, 0, 0 ]

    direction = 0
    while direction < 3:

        # if the raw reading is more than than an average wall distance, set the clear boolean in the array to 1 (clear)
        if LCR_raw[direction] > ultrasonic_wall_sensing_distance:
            LCR_clear_bool[direction] = 1
        direction += 1

    return LCR_clear_bool

# this function causes the bot to loudly exclaim, indicating the can has been recognised
def beeping_flashing():
    while 1:
        Sound.tone([(1000, 500, 500)] * 20)
        Leds.set_color(Leds.RIGHT, Leds.RED)
        Leds.set_color(Leds.LEFT, Leds.RED)
        time.sleep(1)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        time.sleep(1)


#---2. DECISION FUNCTIONS---#
#
# this function returns to booleans to inform the movement of the motors and the orientation of the robot
def movement_decision(route_array):

    #
    #
    # THIS IS WHERE DECISION IS FOUND
    #
    #
    forward = 1
    left = 1

    return forward, left

# this function is just for printing to the output and debugging and will be removed
def print_route_options(route_array):
    # string array to help printable output
    print("- - -")
    direction_strings = ["LEFT: ", "CENTER: ", "RIGHT: "]

    for i in range(len(route_array)):
        print(direction_strings[i])
        if route_array[i] == True:
            print("Clear\n")
        else:
            print("Blocked\n")

    print("- - -\n")


#---3. MOVEMENT FUNCTIONS---#
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


# this function stops both motors
def stop_motors():
    # leftMotor.reset()
    leftMotor.stop()
    # rightMotor.reset()
    rightMotor.stop()

#---MAIN FUNCTION---#
'''
    the main loop of this program will
        move forward a certain distance
        scan in 3 directions
        store each direction results
        print out scan results
'''

while True:
    # 1. scan & colour check
    print("\n#--NEW SCAN BEGINNING--#\n")
    route_array = []            # new array to hold boolean variables to indicate whether routes are clear
    route_array = start_scan()  # call start_scan and also set the route array for the decision function

    # 2. decision function based on scan results
    print_route_options(route_array)  # print to console whether the routes are clear are not
    future_movement = []  # new array to hold variable to indicate movement of decision function
    future_movement = movement_decision(route_array)

    # 3. turn based on value of decision value function
    if future_movement[0] == 1:    # forwards and backwards movement
        move_1_block(True)  # move a block forwards
    elif future_movement[0] == 0:
        move_1_block(False) # move a block backwards
    elif future_movement[0] == -1:
        print("Stationary") # dont move anywhere
