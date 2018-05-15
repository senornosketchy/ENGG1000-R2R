#!/usr/bin/python3

from time import sleep
import sys, os
from ev3dev.ev3 import *

# ---SENSOR INITIALISATION---#
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
us = UltrasonicSensor(INPUT_1)
assert us.connected

us_front = UltrasonicSensor(INPUT_2)
assert us_front.connected
print("Ultrasonic Connected")

# connect color
cs = ColorSensor(INPUT_3)
assert cs.connected
print("Color Connected")

# 2. calibrate and test here
cs.mode = 'RGB-RAW'  # color
gs.mode = 'GYRO-RATE'  # gyro: changing the mode resets the gyro
gs.mode = 'GYRO-ANG'
leftMotor.reset()  # motors
rightMotor.reset()
servo.reset()  # servo
servo.stop()

# ---GLOBAL IMPORTANT SETTINGS---#
front_wall_us_sensing_distance = 18
ultrasonic_wall_sensing_distance = 210
scan_rotation_speed = 200
wheel_rotations_per_block = 818
wheel_turn_rotations_per_turn = 360 * 0.89 * 0.63

# corrections
wall_too_close = 120
wall_too_far = 197

# last_turn
last_turn = 10
left_turn_count = 0


# ---1. SCANNING FUNCTIONS---#
#
# this function controls all the scanning sub-functions
def start_scan():
    # initialise array to hold ultrasonic data raw
    LCR_raw = [0, 0, 0]

    # Center reading
    rotate_sensors(0, 125)
    sleep(0.2)
    can_check(us.value())
    LCR_raw[1] = us.value()

    # Left
    rotate_sensors(-90, scan_rotation_speed)
    sleep(0.2)
    LCR_raw[0] = us.value()

    # Right
    rotate_sensors(90, scan_rotation_speed)
    sleep(0.2)
    LCR_raw[2] = us.value()

    # format the LCR_bool array
    LCR_clear_bool = are_routes_clear(LCR_raw)

    # return a boolean array based on whether directions are clear
    return LCR_clear_bool


# this function rotates the sensors at a certain speed to a relative point
def rotate_sensors(destination, speed):
    # print("rotating sensors to: ", destination)
    servo.run_to_abs_pos(position_sp=destination, speed_sp=speed, ramp_down_sp=90)
    servo.wait_while('running')


# this function checks the value of the colour sensor to see if it has sensed the can
def can_check(us_last):
    difference = us_last - us_front.value()
    sleep(0.1)
    difference2 = us_last - us_front.value()
    sleep(0.1)
    difference3 = us_last - us_front.value()

    if (
            difference > 125 and difference2 > 125 and difference3 > 125) and cs.red >= 6 and us_front.value() <= front_wall_us_sensing_distance:
        print("\nCAN SENSED\n")
        # beeping_flashing()


# this function determines whether the routes are clear based on ultrasonic data
def are_routes_clear(LCR_raw):
    # print("Raw data: ", LCR_raw)

    LCR_clear_bool = [0, 0, 0]

    direction = 0
    while direction < 3:

        # if the raw reading is more than than an average wall distance, set the clear boolean in the array to 1 (clear)
        if LCR_raw[direction] > ultrasonic_wall_sensing_distance:
            LCR_clear_bool[direction] = 1
        direction += 1

    return LCR_clear_bool


# this function causes the bot to loudly exclaim, indicating the can has been recognised
def beeping_flashing():
    Sound.tone([(1000, 500, 500)] * 5)

    while 1:
        Leds.set_color(Leds.RIGHT, Leds.RED)
        Leds.set_color(Leds.LEFT, Leds.RED)
        time.sleep(1)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        time.sleep(1)


# ---2. DECISION FUNCTIONS---#
#
# this function returns to booleans to inform the movement of the motors and the orientation of the robot
def movement_decision(route_array):
    # if the center route is clear
    if route_array[0] == 1: # left moves left
        left = 1
        forward = 1
    elif route_array[2] == 1: # right moves right
        left = 0
        forward = 1
    elif route_array[1] == 1: # forward moves forward
        left = -1
        forward = 1
    else:
        print("NO ROUTE WAS CLEAR")
        forward = 0
        left = -1

    # turn sensor for wall following DIRECTION TEST
    if left == -1:
        if route_array[0] == 0:
            rotate_sensors(-90, 150)
        elif route_array[2] == 1:
            rotate_sensors(90, 150)
    elif left == 1:
        rotate_sensors(90, 150)
    elif left == 0:
        rotate_sensors(-90, 150)

    # last turn count
    global last_turn
    if last_turn != -1:  # only count actual turns
        last_turn = left

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


# ---3. MOVEMENT FUNCTIONS---#
#
# this function moves the bot forward or backwards 1 block
def move_1_block(forward):
    # set_corrections
    current_wall_dist = us.value()
    if (current_wall_dist < wall_too_close):
        print("too close to the wall")
        correct()
    elif (current_wall_dist > wall_too_far and current_wall_dist < ultrasonic_wall_sensing_distance):
        print("too far away from the wall")
        correct()

    spins = wheel_rotations_per_block
    if forward:
        spins = spins * -1

    leftMotor.run_to_rel_pos(position_sp=spins, speed_sp=350, ramp_down_sp=120)
    rightMotor.run_to_rel_pos(position_sp=spins, speed_sp=350, ramp_down_sp=120)

    left_running_state = leftMotor.state
    right_running_state = rightMotor.state
    # wait until motor stops before continuing with anything else
    while (leftMotor.state == left_running_state or rightMotor.state == right_running_state) and forward:
        if us_front.value() < front_wall_us_sensing_distance:
            stop_motors()
            print("Wall was sensed early so motor stopped")
            break


# this function turns 90 degrees
def turn(left):
    # SET DIR PREFIX AND RECORD FIRST ANGLE
    print()
    print("------STARTING TURN------")
    beginning_angle = gs.value()
    if left:
        # assuming that the right (clockwise) dir is positive
        direction_prefix = -1
    else:
        direction_prefix = 1

    # FIND NEAREST 90 IN THE DIRECTION OF TURN
    destination_angle = beginning_angle + (direction_prefix * 45)
    while destination_angle % 90 != 0:
        destination_angle += direction_prefix

    destination_angle = destination_angle + (-direction_prefix * 4)
    print("Destination is ", destination_angle)

    # START DRIVING IN CORRECT DIR
    leftMotor.run_to_rel_pos(position_sp=350 * direction_prefix, speed_sp=200, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=-350 * direction_prefix, speed_sp=200, ramp_down_sp=90)

    run_state = leftMotor.state

    # LOOP TO BREAK ONCE THE GYRO IS IN CORRECT RANGE
    while (gs.value() < destination_angle - 1 and gs.value() < destination_angle + 1) or (
            gs.value() > destination_angle - 1 and gs.value() > destination_angle + 1):
        print(gs.value())
        if leftMotor.state != run_state:
            print("Motor was stopped by rel_pos")
            break

    # STOP MOTORS IMMEDIATELY
    stop_motors()
    print("finishing gyroscopic turn")
    print("Final position is:", gs.value())
    print()
    print("------TURN FINISHED-------")
    print()



def correct():
    print("CORRECTIONS STARTING")

    if last_turn == 1:
        direction = 1
    else:
        direction = -1

    leftMotor.run_to_rel_pos(position_sp=30 * direction, speed_sp=150, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=-30 * direction, speed_sp=150, ramp_down_sp=90)
    leftMotor.wait_while('running')

    leftMotor.run_to_rel_pos(position_sp=70 * direction, speed_sp=150, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=70 * direction, speed_sp=150, ramp_down_sp=90)
    leftMotor.wait_while('running')

    leftMotor.run_to_rel_pos(position_sp=-30 * direction, speed_sp=150, ramp_down_sp=90)
    rightMotor.run_to_rel_pos(position_sp=30 * direction, speed_sp=150, ramp_down_sp=90)
    leftMotor.wait_while('running')


# this function stops both motors
def stop_motors():
    # leftMotor.reset()
    leftMotor.stop()
    # rightMotor.reset()
    rightMotor.stop()


# ---MAIN FUNCTION---#
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
    route_array = []  # new array to hold boolean variables to indicate whether routes are clear
    route_array = start_scan()  # call start_scan and also set the route array for the decision function

    # 2. decision function based on scan results
    print_route_options(route_array)  # print to console whether the routes are clear are not
    future_movement = []  # new array to hold variable to indicate movement of decision function
    future_movement = movement_decision(route_array)

    # 3. turn based on value of decision value function
    #   left / right / none
    if future_movement[1] == 1:
        print("Left")
        turn(True)  # turn 90 left
    elif future_movement[1] == 0:
        print("Right")
        turn(False)  # turn 90 right
    elif future_movement[1] == -1:
        print("Stationary")  # dont move anywhere

    #   forwards / backwards / none
    if future_movement[0] == 1:
        print("Forward")
        move_1_block(True)  # move a block forwards
    elif future_movement[0] == 0:
        print("Back 180")
        if last_turn == 0:
            turn(True)  # turn twice
            turn(True)
            print("left twice")
        else:
            turn(False)
            turn(False)
            print("right twice")
    elif future_movement[0] == -1:
        print("Stationary")  # dont move anywhere

