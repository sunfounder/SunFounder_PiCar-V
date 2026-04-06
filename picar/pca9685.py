"""PCA9685 16-channel PWM driver over I2C."""

import smbus2 as smbus
import time
import math


class PWM:
    _MODE1 = 0x00
    _MODE2 = 0x01
    _PRESCALE = 0xFE
    _LED0_ON_L = 0x06
    _LED0_ON_H = 0x07
    _LED0_OFF_L = 0x08
    _LED0_OFF_H = 0x09
    _ALL_LED_ON_L = 0xFA
    _ALL_LED_ON_H = 0xFB
    _ALL_LED_OFF_L = 0xFC
    _ALL_LED_OFF_H = 0xFD

    _RESTART = 0x80
    _SLEEP = 0x10
    _ALLCALL = 0x01
    _OUTDRV = 0x04

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "pca9685.py":'

    def __init__(self, bus_number=1, address=0x40):
        self.address = address
        self.bus_number = bus_number
        self.bus = smbus.SMBus(self.bus_number)

    def _debug_(self, message):
        if self._DEBUG:
            print(self._DEBUG_INFO, message)

    def setup(self):
        self._debug_("Reseting PCA9685 MODE1 (without SLEEP) and MODE2")
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self._frequency = 60

    def _write_byte_data(self, reg, value):
        self._debug_("Writing value %2X to %2X" % (value, reg))
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as e:
            print(e)
            self._check_i2c()

    def _read_byte_data(self, reg):
        self._debug_("Reading value from %2X" % reg)
        try:
            return self.bus.read_byte_data(self.address, reg)
        except Exception as e:
            print(e)
            self._check_i2c()

    def _check_i2c(self):
        import subprocess
        from os import listdir

        print("I2C bus number is: %s" % self.bus_number)
        devices = listdir("/dev/")
        if "i2c-%d" % self.bus_number in devices:
            print("I2C device exist.")
        else:
            print(
                "Seems like I2C have not been set, "
                "run 'sudo raspi-config' to enable I2C"
            )
        result = subprocess.run(
            ["i2cdetect", "-y", str(self.bus_number)],
            capture_output=True,
            text=True,
        )
        print("Your PCA9685 address is set to 0x%02X" % self.address)
        print("i2cdetect output:")
        print(result.stdout)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        self._debug_("Set frequency to %d" % freq)
        self._frequency = freq
        prescale_value = 25000000.0 / 4096.0 / float(freq) - 1.0
        prescale = math.floor(prescale_value + 0.5)

        old_mode = self._read_byte_data(self._MODE1)
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(prescale))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)

    def write(self, channel, on, off):
        self._debug_('Set channel "%d" to value "%d"' % (channel, off))
        self._write_byte_data(self._LED0_ON_L + 4 * channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H + 4 * channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L + 4 * channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H + 4 * channel, off >> 8)

    def write_all_value(self, on, off):
        self._debug_('Set all channel to value "%d"' % off)
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

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
