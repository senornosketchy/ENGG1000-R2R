#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

btn = Button()

while not btn.backspace:
    print(btn.left)
    sleep(1)
