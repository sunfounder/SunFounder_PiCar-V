#!/usr/bin/env python
'''
**********************************************************************
* Filename    : TB6612.py
* Description : A driver module for TB6612
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-23    New release
**********************************************************************
'''
import RPi.GPIO as GPIO

class Motor(object):
	''' Motor driver class
		Set direction_channel to the GPIO channel which connect to MA, 
		Set motor_B to the GPIO channel which connect to MB,
		Both GPIO channel use BCM numbering;
		Set pwm_channel to the PWM channel which connect to PWMA,
		Set pwm_B to the PWM channel which connect to PWMB;
		PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
		Set debug to True to print out debug informations.
	'''
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "TB6612.py":'

	def __init__(self, direction_channel, pwm=None, offset=True):
		'''Init a motor on giving dir. channel and PWM channel.'''
		self._debug_("Debug on")
		self.direction_channel = direction_channel
		self._pwm = pwm
		self._offset = offset
		self.forward_offset = self._offset

		self.backward_offset = not self.forward_offset
		self._speed = 0

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		self._debug_('setup motor direction channel at %s' % direction_channel)
		self._debug_('setup motor pwm channel')# self._debug_('setup motor pwm channel as %s ' % self._pwm.__name__)
		GPIO.setup(self.direction_channel, GPIO.OUT)

	def _debug_(self,message):
		if self._DEBUG :
			print(self._DEBUG_INFO,message)

	@property
	def speed(self):
		return self._speed

	@speed.setter
	def speed(self, speed):
		''' Set Speed with giving value '''
		if speed not in range(0, 101):
			raise ValueError('speed ranges fron 0 to 100, not "{0}"'.format(speed))
		if not callable(self._pwm):
			raise ValueError('pwm is not callable, please set Motor.pwm to a pwm control function with only 1 veriable speed')
		self._debug_('Set speed to: %s' % speed)
		self._speed = speed
		self._pwm(self._speed)

	def forward(self):
		''' Set the motor direction to forward '''
		GPIO.output(self.direction_channel, self.forward_offset)
		self.speed = self._speed
		self._debug_('Motor moving forward (%s)' % str(self.forward_offset))

	def backward(self):
		''' Set the motor direction to backward '''
		GPIO.output(self.direction_channel, self.backward_offset)
		self.speed = self._speed
		self._debug_('Motor moving backward (%s)' % str(self.backward_offset))

	def stop(self):
		''' Stop the motor by giving a 0 speed '''
		self._debug_('Motor stop')
		self.speed = 0

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, value):
		''' Set offset for much user-friendly '''
		if value not in (True, False):
			raise ValueError('offset value must be Bool value, not"{0}"'.format(value))
		self.forward_offset = value
		self.backward_offset = not self.forward_offset
		self._debug_('Set offset to %d' % self._offset)

	@property
	def debug(self, debug):
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

	@property
	def pwm(self):
		return self._pwm

	@pwm.setter
	def pwm(self, pwm):
		self._debug_('pwm set')
		self._pwm = pwm


def test():
	import time

	print("********************************************")
	print("*                                          *")
	print("*           SunFounder TB6612              *")
	print("*                                          *")
	print("*          Connect MA to BCM17             *")
	print("*          Connect MB to BCM18             *")
	print("*         Connect PWMA to BCM27            *")
	print("*         Connect PWMB to BCM12            *")
	print("*                                          *")
	print("********************************************")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup((27, 22), GPIO.OUT)
	a = GPIO.PWM(27, 60)
	b = GPIO.PWM(22, 60)
	a.start(0)
	b.start(0)

	def a_speed(value):
		a.ChangeDutyCycle(value)

	def b_speed(value):
		b.ChangeDutyCycle(value)

	motorA = Motor(23)
	motorB = Motor(24)
	motorA.debug = True
	motorB.debug = True
	motorA.pwm = a_speed
	motorB.pwm = b_speed

	delay = 0.05

	motorA.forward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorA.backward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorB.forward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)

	motorB.backward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)


if __name__ == '__main__':
	test()
