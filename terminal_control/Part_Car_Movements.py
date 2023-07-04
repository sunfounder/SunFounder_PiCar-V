#!/usr/bin/python3

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

if __name__ == "__main__":
    debug = ''
    
    bw.ready()
    bw_status = 0
    
    fw.turn_straight()
    
    for x in range(0, 1000):
        print(x)
        sleep(5)
        fw.turn_left()
        
        sleep(5)
        fw.turn_right()
        
        sleep(5)
        fw.turn_straight()
        
        sleep(1)
        bw.speed = SPEED
        bw.forward()
        bw_status = 1
        debug = "speed =", SPEED
        
        sleep(1)
        bw.stop()
        bw_status = 0

        sleep(1)
        bw.speed = SPEED
        bw.backward()
        bw_status = -1

        sleep(1)
        bw.stop()
        bw_status = 0