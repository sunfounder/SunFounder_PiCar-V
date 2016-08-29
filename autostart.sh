#!/bin/sh

cd /home/pi/SunFounder_Smart_Video_Car_Kit_V2.0_for_Raspberry_Pi/remote_control

sudo nohup ./start > log/start.log 2>&1 &
