# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from server import camera, back_wheels, front_wheels, stream
from django.http import HttpResponse

fw = front_wheels.Front_Wheels()
bw = back_wheels.Back_Wheels()
cam = camera.Camera()
cam.ready()
fw.ready()
bw.ready()

SPEED = 60
bw_status = 0

try:
	stream.on()
except:
	pass

def home(request):
	return render_to_response("base.html", request)

def run(request):
	global SPEED, bw_status
	debug = ''
	if 'action' in request.GET:
		action = request.GET['action']
		# ============== Back wheels =============
		if action == 'bwready':
			bw.ready()
			bw_status = 0
		elif action == 'forward':
			bw.set_speed(SPEED)
			bw.forward()
			bw_status = 1
			debug = "speed =", SPEED
		elif action == 'backward':
			bw.set_speed(SPEED)
			bw.backward()
			bw_status = -1
		elif action == 'stop':
			bw.stop()
			bw_status = 0

		# ============== Front wheels =============
		elif action == 'fwready':
			fw.ready()
		elif action == 'fwleft':
			fw.turn_left()
		elif action == 'fwright':
			fw.turn_right()
		elif action == 'fwstraight':
			fw.turn_straight()

		# ================ Camera =================
		elif action == 'camready':
			cam.ready()
		elif action == "camleft":
			cam.turn_left(40)
		elif action == 'camright':
			cam.turn_right(40)
		elif action == 'camup':
			cam.turn_up(20)
		elif action == 'camdown':
			cam.turn_down(20)	
	if 'speed' in request.GET:
		speed = int(request.GET['speed'])
		if speed < 0:
			speed = 0
		if speed > 100:
			speed = 100
		SPEED = speed
		if bw_status != 0:
			bw.set_speed(SPEED)
		debug = "speed =", speed
	host = stream.get_host()[:-2]
	return render_to_response("run.html", {'host': host})

def cali(request):
	if 'action' in request.GET:
		action = request.GET['action']
		# ========== Camera calibration =========
		if action == 'camcali':
			print '"%s" command received' % action
			cam.calibration()
		elif action == 'camcaliup':
			print '"%s" command received' % action
			cam.cali_up()
		elif action == 'camcalidown':
			print '"%s" command received' % action
			cam.cali_down()
		elif action == 'camcalileft':
			print '"%s" command received' % action
			cam.cali_left()
		elif action == 'camcaliright':
			print '"%s" command received' % action
			cam.cali_right()
		elif action == 'camcaliok':
			print '"%s" command received' % action
			cam.cali_ok()

		# ========= Front wheel cali ===========
		elif action == 'fwcali':
			print '"%s" command received' % action
			fw.calibration()
		elif action == 'fwcalileft':
			print '"%s" command received' % action
			fw.cali_left()
		elif action == 'fwcaliright':
			print '"%s" command received' % action
			fw.cali_right()
		elif action == 'fwcaliok':
			print '"%s" command received' % action
			fw.cali_ok()

		# ========= Back wheel cali ===========
		elif action == 'bwcali':
			print '"%s" command received' % action
			bw.calibration()
		elif action == 'bwcalileft':
			print '"%s" command received' % action
			bw.cali_left()
		elif action == 'bwcaliright':
			print '"%s" command received' % action
			bw.cali_right()
		elif action == 'bwcaliok':
			print '"%s" command received' % action
			bw.cali_ok()
		else:
			print 'command error, error command "%s" received' % action
	return render_to_response("cali.html", request)

def connection_test(request):
	return HttpResponse('OK')