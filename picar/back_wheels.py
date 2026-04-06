"""Back wheels (motor) control via TB6612 + PCA9685 PWM."""

from . import tb6612
from . import pca9685
from . import filedb


class Back_Wheels:
    Motor_A = 17
    Motor_B = 27

    PWM_A = 4
    PWM_B = 5

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "back_wheels.py":'

    def __init__(self, debug=False, bus_number=1, db="config"):
        self.forward_A = True
        self.forward_B = True

        self.db = filedb.fileDB(db=db)

        self.forward_A = int(self.db.get("forward_A", default_value=1))
        self.forward_B = int(self.db.get("forward_B", default_value=1))

        self.left_wheel = tb6612.Motor(self.Motor_A, offset=self.forward_A)
        self.right_wheel = tb6612.Motor(self.Motor_B, offset=self.forward_B)

        self.pwm = pca9685.PWM(bus_number=bus_number)

        def _set_a_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_A, 0, pulse_wide)

        def _set_b_pwm(value):
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_B, 0, pulse_wide)

        self.left_wheel.pwm = _set_a_pwm
        self.right_wheel.pwm = _set_b_pwm

        self._speed = 0
        self.debug = debug
        self._debug_(
            "Set left wheel to #%d, PWM channel to %d" % (self.Motor_A, self.PWM_A)
        )
        self._debug_(
            "Set right wheel to #%d, PWM channel to %d" % (self.Motor_B, self.PWM_B)
        )

    def _debug_(self, message):
        if self._DEBUG:
            print(self._DEBUG_INFO, message)

    def forward(self):
        self.left_wheel.forward()
        self.right_wheel.forward()
        self._debug_("Running forward")

    def backward(self):
        self.left_wheel.backward()
        self.right_wheel.backward()
        self._debug_("Running backward")

    def stop(self):
        self.left_wheel.stop()
        self.right_wheel.stop()
        self._debug_("Stop")

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        self.left_wheel.speed = self._speed
        self.right_wheel.speed = self._speed
        self._debug_("Set speed to %s" % self._speed)

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
        self.left_wheel.offset = self.forward_A
        self.right_wheel.offset = self.forward_B
        self.stop()

    def calibration(self):
        self._debug_('Turn to "Calibration" position')
        self.speed = 50
        self.forward()
        self.cali_forward_A = self.forward_A
        self.cali_forward_B = self.forward_B

    def cali_left(self):
        self.cali_forward_A = (1 + self.cali_forward_A) & 1
        self.left_wheel.offset = self.cali_forward_A
        self.forward()

    def cali_right(self):
        self.cali_forward_B = (1 + self.cali_forward_B) & 1
        self.right_wheel.offset = self.cali_forward_B
        self.forward()

    def cali_ok(self):
        self.forward_A = self.cali_forward_A
        self.forward_B = self.cali_forward_B
        self.db.set("forward_A", self.forward_A)
        self.db.set("forward_B", self.forward_B)
        self.stop()
