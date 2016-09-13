#!/bin/sh
#*********************************************************************
# Filename    : autostart.sh
# Description : Auto start script
# Author      : Dream
# Brand       : SunFounder
# E-mail      : service@sunfounder.com
# Website     : www.sunfounder.com
# Update      : Dream    2016-09-13    New release
#*********************************************************************

cd /home/pi/SunFounder_Smart_Video_Car_Kit_V2.0_for_Raspberry_Pi/remote_control

sudo nohup ./start > log/start.log 2>&1 &
