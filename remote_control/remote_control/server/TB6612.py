import RPi.GPIO as GPIO
import PCA9685

class Motor(object):

	# Set direction_channel to the GPIO channel which connect to MA, 
	# Set motor_B to the GPIO channel which connect to MB,
	# Both GPIO channel use BCM numbering;
	# Set pwm_channel to the PWM channel which connect to PWMA,
	# Set pwm_B to the PWM channel which connect to PWMB;
	# PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
	# Set debug to True to print out debug informations.
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "TB6612.py":'

	def __init__(self, direction_channel, pwm_channel, pwm_address=0x40, offset=True):
		if self._DEBUG:
			print self._DEBUG_INFO, "Debug on"
		self.direction_channel = direction_channel
		self.pwm_channel = pwm_channel
		self.offset = offset
		self.forward_offset = self.offset

		self.backward_offset = not self.forward_offset

		self.pwm = PCA9685.PWM(address=pwm_address)
		self.set_debug(self._DEBUG)
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		if self._DEBUG:
			print self._DEBUG_INFO, 'setup motor direction channel at', direction_channel
			print self._DEBUG_INFO, 'setup motor pwm channel at', pwm_channel
		GPIO.setup(self.direction_channel, GPIO.OUT)

	def _map(self, x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	def set_speed(self, speed):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set speed to: ', speed
		self.speed = self._map(speed, 0, 100, 0, 4095)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Speed pwm: ', speed
		self.pwm.set_value(self.pwm_channel, 0, self.speed)

	def forward(self):
		GPIO.output(self.direction_channel, self.forward_offset)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving forward (%s)' % str(self.forward_offset)

	def backward(self):
		GPIO.output(self.direction_channel, self.backward_offset)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving backward (%s)' % str(self.backward_offset)

	def stop(self):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor stop'
		self.set_speed(0)

	def set_offset(self, value):
		if value not in (True, False):
			raise ValueError('offset value must be Bool value, not"{0}"').format(value)
		self.forward_offset = value
		self.backward_offset = not self.forward_offset
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set offset to %d' % self.offset

	def set_debug(self, debug):
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
		else:
			print self._DEBUG_INFO, "Set debug off"