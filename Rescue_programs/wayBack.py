from ev3.lego import Motor

c = Motor(port = Motor.PORT.C)

from arrays import *

while btn.any():
    
    initialMotorLocation= c.read_value("position")
    # while can not found
        #code in choosing the direction
        if direction == forward:
            wayBack[movementNumber] = forward();
        elif direction == left:
            wayBack[movementNumber] = turn(right);
        elif direction == right:
            wayBack[movementNumber] = turn(left);
        #code in moving the bot    

def headingback(movementNumber,initialMotorLocation,wayBack[]):
    turn(left);
    turn(left);
    i = movementNumber;
    while c.read_value("position") != initialMotorLocation or i != 0:
        wayBack[i];
        i = i - 1;

