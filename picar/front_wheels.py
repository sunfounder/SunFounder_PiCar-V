"""Front wheels (steering) control via servo."""

from . import servo
from . import filedb


class Front_Wheels:
    FRONT_WHEEL_CHANNEL = 0

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "front_wheels.py":'

    def __init__(self, debug=False, db="config", bus_number=1, channel=FRONT_WHEEL_CHANNEL):
        self.db = filedb.fileDB(db=db)
        self._channel = channel
        self._straight_angle = 90
        self.turning_max = 45
        self._turning_offset = int(
            self.db.get("turning_offset", default_value=0)
        )

        self.wheel = servo.Servo(
            self._channel, bus_number=bus_number, offset=self.turning_offset
        )
        self.debug = debug
        self._debug_("Front wheel PWM channel: %s" % self._channel)
        self._debug_("Front wheel offset value: %s " % self.turning_offset)

        self._angle = {
            "left": self._min_angle,
            "straight": self._straight_angle,
            "right": self._max_angle,
        }

    def _debug_(self, message):
        if self._DEBUG:
            print(self._DEBUG_INFO, message)

    def turn_left(self):
        self._debug_("Turn left")
        self.wheel.write(self._angle["left"])

    def turn_straight(self):
        self._debug_("Turn straight")
        self.wheel.write(self._angle["straight"])

    def turn_right(self):
        self._debug_("Turn right")
        self.wheel.write(self._angle["right"])

    def turn(self, angle):
        self._debug_("Turn to %s " % angle)
        angle = max(self._angle["left"], min(self._angle["right"], angle))
        self.wheel.write(angle)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, chn):
        self._channel = chn

    @property
    def turning_max(self):
        return self._turning_max

    @turning_max.setter
    def turning_max(self, angle):
        self._turning_max = angle
        self._min_angle = self._straight_angle - angle
        self._max_angle = self._straight_angle + angle
        self._angle = {
            "left": self._min_angle,
            "straight": self._straight_angle,
            "right": self._max_angle,
        }

    @property
    def turning_offset(self):
        return self._turning_offset

    @turning_offset.setter
    def turning_offset(self, value):
        if not isinstance(value, int):
            raise TypeError('"turning_offset" must be "int"')
        self._turning_offset = value
        self.db.set("turning_offset", value)
        self.wheel.offset = value
        self.turn_straight()

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

    def ready(self):
        self._debug_('Turn to "Ready" position')
        self.wheel.offset = self.turning_offset
        self.turn_straight()

    def calibration(self):
        self._debug_('Turn to "Calibration" position')
        self.turn_straight()
        self.cali_turning_offset = self.turning_offset

    def cali_left(self):
        self.cali_turning_offset -= 1
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()

    def cali_right(self):
        self.cali_turning_offset += 1
        self.wheel.offset = self.cali_turning_offset
        self.turn_straight()

    def cali_ok(self):
        self.turning_offset = self.cali_turning_offset
        self.db.set("turning_offset", self.turning_offset)
