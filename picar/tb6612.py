"""TB6612FNG motor driver using lgpio (Trixie-compatible)."""

import lgpio


# Share a single gpiochip handle across all Motor instances.
_chip = None


def _get_chip():
    global _chip
    if _chip is None:
        _chip = lgpio.gpiochip_open(0)
    return _chip


class Motor:
    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "tb6612.py":'

    def __init__(self, direction_channel, pwm=None, offset=True):
        self.direction_channel = direction_channel
        self._pwm = pwm
        self._offset = offset
        self.forward_offset = self._offset
        self.backward_offset = not self.forward_offset
        self._speed = 0

        chip = _get_chip()
        lgpio.gpio_claim_output(chip, self.direction_channel)
        self._debug_(
            "setup motor direction channel at %s" % direction_channel
        )

    def _debug_(self, message):
        if self._DEBUG:
            print(self._DEBUG_INFO, message)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed not in range(0, 101):
            raise ValueError(
                'speed ranges from 0 to 100, not "%s"' % speed
            )
        if not callable(self._pwm):
            raise ValueError(
                "pwm is not callable, please set Motor.pwm to a "
                "pwm control function with only 1 variable speed"
            )
        self._debug_("Set speed to: %s" % speed)
        self._speed = speed
        self._pwm(self._speed)

    def forward(self):
        chip = _get_chip()
        lgpio.gpio_write(chip, self.direction_channel, int(self.forward_offset))
        self.speed = self._speed
        self._debug_("Motor moving forward (%s)" % self.forward_offset)

    def backward(self):
        chip = _get_chip()
        lgpio.gpio_write(chip, self.direction_channel, int(self.backward_offset))
        self.speed = self._speed
        self._debug_("Motor moving backward (%s)" % self.backward_offset)

    def stop(self):
        self._debug_("Motor stop")
        self.speed = 0

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        if value not in (True, False, 0, 1):
            raise ValueError(
                'offset value must be Bool value, not "%s"' % value
            )
        self.forward_offset = bool(value)
        self.backward_offset = not self.forward_offset
        self._debug_("Set offset to %s" % self._offset)

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

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm):
        self._debug_("pwm set")
        self._pwm = pwm
