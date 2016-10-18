#!/usr/bin/env python
'''
**********************************************************************
* Filename    : Servo.py
* Description : Driver module for servo, with PCA9685
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
**********************************************************************
'''

import PCA9685

def _map(x, in_min, in_max, out_min, out_max):
	'''To map the value from arange to another'''
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Servo(object):
	'''Servo driver class'''
	_MIN_PULSE_WIDTH = 600
	_MAX_PULSE_WIDTH = 2400
	_DEFAULT_PULSE_WIDTH = 1500
	_FREQUENCY = 60

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "Servo.py":'

	def __init__(self, channel, offset=0, lock=True):
		''' Init a servo on specific channel, this offset '''
		if channel<0 or channel > 16:
			raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(channel))
		if self._DEBUG:
			print self._DEBUG_INFO, "Debug on"
		self.channel = channel
		self.offset = offset
		self.lock = lock

		self.pwm = PCA9685.PWM()
		self.pwm.set_frequency(60)
		self.pwm.set_value(self.channel, 0, self._DEFAULT_PULSE_WIDTH)

	def _angle_to_analog(self, angle):
		''' Calculate 12-bit analog value from giving angle '''
		pulse_wide   = _map(angle, 0, 180, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
		analog_value = int(float(pulse_wide) / 1000000 * self._FREQUENCY * 4096)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Angle %d equals Analog_value %d' % (angle, analog_value)
		return analog_value
		
	def set_offset(self, value):
		''' Set offset for much user-friendly '''
		self.offset = value
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set offset to %d' % self.offset

	def turn(self, angle):
		''' Turn the servo with giving angle. '''
		if self.lock:
			if angle > 180:
				angle = 180
			if angle < 0:
				angle = 0
		else:
			if angle<0 or angle>180:
				raise ValueError("Servo \"{0}\" turn angle \"{1}\" is not in (0, 180).".format(self.channel, angle))
		val = self._angle_to_analog(angle)
		val += self.offset
		self.pwm.set_value(self.channel, 0, val)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn angle = %d' % angle

	def set_debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
		else:
			print self._DEBUG_INFO, "Set debug off"

def test():
	'''Servo driver test on channel 1'''
	import time
	a = Servo(1)
	for i in range(0, 180, 5):
		print i
		a.turn(i)
		time.sleep(0.1)
	for i in range(180, 0, -5):
		print i
		a.turn(i)
		time.sleep(0.1)
	for i in range(0, 91, 2):
		a.turn(i)
		time.sleep(0.05)
	print i

if __name__ == '__main__':
	test()
