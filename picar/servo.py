"""Servo driver using PCA9685 PWM controller."""

from . import pca9685


class Servo:
    _MIN_PULSE_WIDTH = 600
    _MAX_PULSE_WIDTH = 2400
    _DEFAULT_PULSE_WIDTH = 1500
    _FREQUENCY = 60

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "servo.py":'

    def __init__(self, channel, offset=0, lock=True, bus_number=1, address=0x40):
        if channel < 0 or channel > 16:
            raise ValueError(
                'Servo channel "%d" is not in (0, 15).' % channel
            )
        self.channel = channel
        self._offset = offset
        self.lock = lock

        self.pwm = pca9685.PWM(bus_number=bus_number, address=address)
        self.frequency = self._FREQUENCY
        self.write(90)

    def _debug_(self, message):
        if self._DEBUG:
            print(self._DEBUG_INFO, message)

    def setup(self):
        self.pwm.setup()

    def _angle_to_analog(self, angle):
        pulse_wide = self.pwm.map(
            angle, 0, 180, self._MIN_PULSE_WIDTH, self._MAX_PULSE_WIDTH
        )
        analog_value = int(float(pulse_wide) / 1000000 * self.frequency * 4096)
        self._debug_("Angle %d equals Analog_value %d" % (angle, analog_value))
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
        self._offset = value
        self._debug_("Set offset to %d" % self._offset)

    def _pulse_to_analog(self, pulse_wide):
        return int(float(pulse_wide) / 1000000 * self.frequency * 4096)

    def write(self, angle):
        if self.lock:
            angle = max(0, min(180, angle))
        elif angle < 0 or angle > 180:
            raise ValueError(
                'Servo "%d" turn angle "%d" is not in (0, 180).'
                % (self.channel, angle)
            )
        val = self._angle_to_analog(angle)
        val += self._offset
        # The offset is applied after the angle clamp above, so a non-zero
        # offset can push the final pulse outside the servo's rated range
        # and drive it into its mechanical stop, where it stalls and buzzes.
        # Clamp in the analog domain, which is what actually reaches the servo.
        low = self._pulse_to_analog(self._MIN_PULSE_WIDTH)
        high = self._pulse_to_analog(self._MAX_PULSE_WIDTH)
        clamped = max(low, min(high, val))
        if clamped != val:
            self._debug_(
                "Analog value %d out of range (%d, %d); clamped to %d"
                % (val, low, high, clamped)
            )
        self.pwm.write(self.channel, 0, clamped)
        self._debug_("Turn angle = %d" % angle)

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError(
                'debug must be True or False, not "%s"' % debug
            )
