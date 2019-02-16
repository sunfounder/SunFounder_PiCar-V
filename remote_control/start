#!/bin/sh
#**********************************************************************
#* Filename    : start
#* Description : a simple bash script to run the django server
#* Author      : Cavon
#* Brand       : SunFounder
#* E-mail      : service@sunfounder.com
#* Website     : www.sunfounder.com
#* Update      : Cavon    2016-09-13    New release
#*               Cavon    2016-10-19    Add install config
#**********************************************************************

if [ "$1" = "" ]
then
	# Run server listen to any IP address and port 8000
	echo "Server running"
	python3 manage.py runserver 0.0.0.0:8000
elif [ "$1" = "install" ]
then
	echo 'Running servo installation'
	python3 remote_control/driver/Servo.py install
fi
