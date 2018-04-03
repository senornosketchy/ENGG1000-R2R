# Import a few system libraries that will be needed
from time import sleep
import sys, os
import matplotlib.pyplot as plt

# Import the ev3dev specific library
from ev3dev.ev3 import *

# Connect motors
rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_C)

# Connect touch sensors.

us = UltrasonicSensor();
assert us.connected

# We will need to check EV3 buttons state.
btn = Button()


def start(left, right):
    """
    Start both motors at the given speeds.
    """
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)


def stop():
    # Stop both motors
    leftMotor.stop(stop_action='brake')
    rightMotor.stop(stop_action='brake')


# Run the robot until a button is pressed.

ultrasonicValues = []
while not btn.any():
    ultrasonicValues.append(us.value())
    start(50, 50)

fig1 = plt.figure()         # create a new figure
plt.plot(range(len(ultrasonicValues)), ultrasonicValues)       # plot(data in x-axis, data in y-axis)
plt.xlabel('Time (not in any units cos it\'s not actually time)')    # label for x-axis
plt.ylabel('Distance (ms)')   # label for y-axis
plt.title('US value vs Time')  # title of the graph
plt.grid()  # display the grid
plt.show()  # to display the graph
fig1.savefig('ultrasonic.png')  # save the graph as a PNG file
# Stop the motors before exiting.
stop()
