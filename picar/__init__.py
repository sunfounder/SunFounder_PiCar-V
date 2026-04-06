"""Vendored picar library for SunFounder PiCar-V.

Ported from https://github.com/sunfounder/SunFounder_PiCar for
Debian Trixie (Python 3.13, lgpio instead of RPi.GPIO).
"""

from . import front_wheels, back_wheels
from . import pca9685, servo


def setup():
    pwm = pca9685.PWM(bus_number=1)
    pwm.setup()
    pwm.frequency = 60
