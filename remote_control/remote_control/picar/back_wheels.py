#!/usr/bin/env python
'''
**********************************************************************
* Filename    : back_wheels.py
* Description : A module to control the back wheels of RPi Car
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
*               Cavon    2016-11-04    fix for submodules
**********************************************************************
'''

from .SunFounder_TB6612 import TB6612
from .SunFounder_PCA9685 import PCA9685
from .import filedb

class Back_Wheels(object):
	''' Back wheels control class '''
	Motor_A = 17
	Motor_B = 27

	PWM_A = 4
	PWM_B = 5

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "back_wheels.py":'

	def __init__(self, debug=False, bus_number=1, db="config"):
		''' Init the direction channel and pwm channel '''
		self.forward_A = True
		self.forward_B = True

		self.db = filedb.fileDB(db=db)

		self.forward_A = int(self.db.get('forward_A', default_value=1))
		self.forward_B = int(self.db.get('forward_B', default_value=1))

		self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.forward_A)
		self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.forward_B)

		self.pwm = PCA9685.PWM(bus_number=bus_number)
		def _set_a_pwm(value):
			pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
			self.pwm.write(self.PWM_A, 0, pulse_wide)

		def _set_b_pwm(value):
			pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
			self.pwm.write(self.PWM_B, 0, pulse_wide)

		self.left_wheel.pwm  = _set_a_pwm
		self.right_wheel.pwm = _set_b_pwm

		self._speed = 0

		self.debug = debug
		self._debug_('Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A))
		self._debug_('Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B))

	def _debug_(self,message):
		if self._DEBUG:
			print(self._DEBUG_INFO,message)

	def forward(self):
		''' Move both wheels forward '''
		self.left_wheel.forward()
		self.right_wheel.forward()
		self._debug_('Running forward')

	def backward(self):
		''' Move both wheels backward '''
		self.left_wheel.backward()
		self.right_wheel.backward()
		self._debug_('Running backward')

	def stop(self):
		''' Stop both wheels '''
		self.left_wheel.stop()
		self.right_wheel.stop()
		self._debug_('Stop')

	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._speed = speed
		''' Set moving speeds '''
		self.left_wheel.speed = self._speed
		self.right_wheel.speed = self._speed
		self._debug_('Set speed to %s' % self._speed)

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
			self.left_wheel.debug = True
			self.right_wheel.debug = True
			self.pwm.debug = True
		else:
			print(self._DEBUG_INFO, "Set debug off")
			self.left_wheel.debug = False
			self.right_wheel.debug = False
			self.pwm.debug = False

	def ready(self):
		''' Get the back wheels to the ready position. (stop) '''
		self._debug_('Turn to "Ready" position')
		self.left_wheel.offset = self.forward_A
		self.right_wheel.offset = self.forward_B
		self.stop()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		self._debug_('Turn to "Calibration" position')
		self.speed = 50
		self.forward()
		self.cali_forward_A = self.forward_A
		self.cali_forward_B = self.forward_B

	def cali_left(self):
		''' Reverse the left wheels forward direction in calibration '''
		self.cali_forward_A = (1 + self.cali_forward_A) & 1
		self.left_wheel.offset = self.cali_forward_A
		self.forward()

	def cali_right(self):
		''' Reverse the right wheels forward direction in calibration '''
		self.cali_forward_B = (1 + self.cali_forward_B) & 1
		self.right_wheel.offset = self.cali_forward_B
		self.forward()

	def cali_ok(self):
		''' Save the calibration value '''
		self.forward_A = self.cali_forward_A
		self.forward_B = self.cali_forward_B
		self.db.set('forward_A', self.forward_A)
		self.db.set('forward_B', self.forward_B)
		self.stop()

def test():
	import time
	back_wheels = Back_Wheels()
	DELAY = 0.01
	try:
		back_wheels.forward()
		for i in range(0, 100):
			back_wheels.speed = i
			print("Forward, speed =", i)
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.speed = i
			print("Forward, speed =", i)
			time.sleep(DELAY)

		back_wheels.backward()
		for i in range(0, 100):
			back_wheels.speed = i
			print("Backward, speed =", i)
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.speed = i
			print("Backward, speed =", i)
			time.sleep(DELAY)
	except KeyboardInterrupt:
		print("KeyboardInterrupt, motor stop")
		back_wheels.stop()
	finally:
		print("Finished, motor stop")
		back_wheels.stop()

if __name__ == '__main__':
	test()
