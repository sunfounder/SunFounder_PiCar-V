#!/usr/bin/env python
'''
**********************************************************************
* Filename    : PCF8591
* Description : A module to read the analog value with ADC PCF8591
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-19    New release
**********************************************************************
'''
import smbus
import time


class PCF8591(object):
    """ Light_Follow Module class """
    AD_CHANNEL = [0x43, 0x42, 0x41, 0x40]

    RPI_REVISION_0 = ["900092"]
    RPI_REVISION_1_MODULE_B  = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
    RPI_REVISION_1_MODULE_A  = ["0007", "0008", "0009",]
    RPI_REVISION_1_MODULE_BP = ["0010", "0013"]
    RPI_REVISION_1_MODULE_AP = ["0012"]
    RPI_REVISION_2_MODULE_B  = ["a01041", "a21041"]
    RPI_REVISION_3_MODULE_B  = ["a02082", "a22082"]
    RPI_REVISION_3_MODULE_BP = ["a020d3"]

    def __init__(self, address=0x48, bus_number=1):
        self.address = address
        self._bus_number = bus_number
        self.bus = smbus.SMBus(self._bus_number)

    def read(self, chn): #channel
        self.bus.write_byte(self.address, self.AD_CHANNEL[chn])
        self.bus.read_byte(self.address) # dummy read to start conversion
        return self.bus.read_byte(self.address)

    @property
    def A0(self):
        return self.read(0)
    @property
    def A1(self):
        return self.read(1)
    @property
    def A2(self):
        return self.read(2)
    @property
    def A3(self):
        return self.read(3)

    def _get_bus_number(self):
        return 1

    def _get_pi_revision(self):
        "Gets the version number of the Raspberry Pi board"
        # Courtesy quick2wire-python-api
        # https://github.com/quick2wire/quick2wire-python-api
        # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line.startswith('Revision'):
                    if line[11:-1] in self.RPI_REVISION_0:
                        return '0'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_B:
                        return '1 Module B'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_A:
                        return '1 Module A'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_BP:
                        return '1 Module B+'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_AP:
                        return '1 Module A+'
                    elif line[11:-1] in self.RPI_REVISION_2_MODULE_B:
                        return '2 Module B'
                    elif line[11:-1] in self.RPI_REVISION_3_MODULE_B:
                        return '3 Module B'
                    elif line[11:-1] in self.RPI_REVISION_3_MODULE_BP:
                        return '3 Module B+'
                    else:
                        print("Error. Pi revision didn't recognize, module number: %s" % line[11:-1])
                        print('Exiting...')
                        quit()
        except Exception as e:
            f.close()
            print(e)
            print('Exiting...')
            quit()
        finally:
            f.close()

def test():
    ADC = PCF8591(0x48)
    while True:
        A0 = ADC.read(0)
        A1 = ADC.read(1)
        A2 = ADC.read(2)

        print("A0 = %d  A1 = %d  A2 = %d"%(A0,A1,A2))
        time.sleep(0.5)

def destroy():
    pass

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        destroy()
