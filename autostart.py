#!/usr/bin/env python
import os

DIR_='/home/pi/video_car_kit'
_SERVER_= 'sudo nohup python %s/server/server.py > %s/server/log/server.log &' %(_DIR_, _DIR_)
try:
	os.system(_SERVER_)
except Exception, e:
	cmd = "echo " + e + " > " + _BOX_DIR_ + "log/log"
	os.system(cmd)
	#print e

