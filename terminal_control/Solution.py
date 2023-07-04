#!/usr/bin/python3

import curses
from picar import back_wheels, front_wheels
from time import sleep

fw = front_wheels.Front_Wheels(debug=False)
bw = back_wheels.Back_Wheels(debug=False)
bw.ready()
fw.ready()

global SPEED 
SPEED= 60
global bw_status
bw_status = 0

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
            screen.addstr(0, 0, 'right')
            fw.turn_right()
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')
            fw.turn_left()
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'up   ')
            fw.turn_straight()
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'down ')
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()