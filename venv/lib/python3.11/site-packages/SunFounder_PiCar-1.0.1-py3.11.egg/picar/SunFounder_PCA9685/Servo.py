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
*               Cavon    2016-09-21    Change channel from 1 to all
**********************************************************************
'''

from . import PCA9685

class Servo(object):
	'''Servo driver class'''
	_MIN_PULSE_WIDTH = 600
	_MAX_PULSE_WIDTH = 2400
	_DEFAULT_PULSE_WIDTH = 1500
	_FREQUENCY = 60

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "Servo.py":'

	def __init__(self, channel, offset=0, lock=True, bus_number=1, address=0x40):
		''' Init a servo on specific channel, this offset '''
		if channel<0 or channel > 16:
			raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(channel))
		self._debug_("Debug on")
		self.channel = channel
		self.offset = offset
		self.lock = lock

		self.pwm = PCA9685.PWM(bus_number=bus_number, address=address)
		self.frequency = self._FREQUENCY
		self.write(90)
	
	def _debug_(self,message):
		if self._DEBUG:
			print(self._DEBUG_INFO,message)

	def setup(self):
		self.pwm.setup()

	def _angle_to_analog(self, angle):
		''' Calculate 12-bit analog value from giving angle '''
		pulse_wide   = self.pwm.map(angle, 0, 180, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH)
		analog_value = int(float(pulse_wide) / 1000000 * self.frequency * 4096)
		self._debug_('Angle %d equals Analog_value %d' % (angle, analog_value))
		return analog_value

	@property
	def frequency(self):
		return self._frequency

	@frequency.setter
	def frequency(self, value):
		self._frequency = value
		self.pwm.frequency = value

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, value):
		''' Set offset for much user-friendly '''
		self._offset = value
		self._debug_('Set offset to %d' % self.offset)

	def write(self, angle):
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
		self.pwm.write(self.channel, 0, val)
		self._debug_('Turn angle = %d' % angle)

	@property
	def debug(self):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print(self._DEBUG_INFO, "Set debug on")
		else:
			print(self._DEBUG_INFO, "Set debug off")

def test():
	'''Servo driver test on channel 1'''
	import time
	a = Servo(1)
	a.setup()
	for i in range(0, 180, 5):
		print(i)
		a.write(i)
		time.sleep(0.1)
	for i in range(180, 0, -5):
		print(i)
		a.write(i)
		time.sleep(0.1)
	for i in range(0, 91, 2):
		a.write(i)
		time.sleep(0.05)
	print(i)

def install():
	all_servo = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
	for i in range(16):
		all_servo[i] = Servo(i)
	for servo in all_servo:
		servo.setup()
		servo.write(90)

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		if sys.argv[1] == "install":
			install()
	else:
		test()
