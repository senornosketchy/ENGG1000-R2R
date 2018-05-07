from ev3.lego import Motor
c = Motor(port = Motor.PORT.C)
from arrays import *

initialMotorLocation= c.read_value("position")

def wayBack(direction,movementNumber):
    if direction == forward:
        wayBack[movementNumber] = forward();
    else if direction == left:
        wayBack[movementNumber] = turn(right);
    else if direction == right:
        wayBack[movementNumber] = turn(left);


def headingback():
    while c.read_value("position") != initialMotorLocation or i != 0:
        wayBack[i];
        i = i + 1;
