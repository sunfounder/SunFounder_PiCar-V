Appendix 2: Components 
======================

Robot HATS
----------

.. image:: media/image120.png
   :width: 400
   :align: center

**Robot HATS** is a specially-designed HAT for a 40-pin Raspberry Pi and
can work with Raspberry Pi model B+, 2 model B, 3 model B, 3 model B+,
and 4 model B. It supplies power to the Raspberry Pi from the GPIO
ports. Thanks to the design of the ideal diode based on the rules of
HATS, it can supply the Raspberry Pi via both the USB cable and the DC
port thus protecting it from damaging the TF card caused by batteries
running out of power. The PCF8591 is used as the ADC chip, with I2C
communication, and the address 0x48.

.. image:: media/image121.jpeg
   :width: 500
   :align: center

1. **Digital ports**: 3-wire digital sensor ports, signal voltage: 3.3V,
   VCC voltage: 3.3V.

2. **Analog ports**: 3-wire 4-channel 8-bit ADC sensor port, reference
   voltage: 3.3V, VCC voltage: 3.3V.

3. **I2C ports**: 3.3V I2C bus ports

4. **5V power output**: 5V power output to PWM driver.

5. **UART port**: 4-wire UART port, 5V VCC, perfectly working with
   SunFounder FTDI Serial to USB.

6. **Motor control ports**: 5V for motors, direction control of motors
   MA and MB and a floating pin NC ; working with SunFounder motor driver
   module.

7. **Switch**: power switch

8. **Power indicators**: indicating the voltage – 2 indicators on:
   >7.9V; 1 indicator on: 7.9V~7.4V; no indicator on: <7.4V. To protect the
   batteries, you're recommended to take them out for charge when there is
   no indicator on. The power indicators depend on the voltage
   measured by the simple comparator circuit; the detected voltage may be
   lower than normal depending on loads, so it is just for reference.

9. **Power port**: 5.5/2.1mm standard DC port, input voltage: 8.4~7.4V
   (limited operating voltage: 12V~6V).

PCA9865
-------

.. image:: media/image122.jpeg
   :width: 500
   :align: center

PCA9685 16-channel 12-bit I2C Bus PWM driver. It supports independent
PWM output power and is easy to use 4-wire I2C port for connection in
parallel, distinguished 3-color ports for PWM output.

.. image:: media/image123.jpeg
   :width: 500
   :align: center

1. **PWM output ports**: 3-color ports, independent power PWM output
   port, connect to the servo directly.

2 and 3. **I2C port**: 4-wire I2C port, can be used in parallel. Compatible with 3.3V/5.5V.

4. **PWM power input**: 12V max.

5. **LED**: power indicator for the chip and for the PWM power input.

Motor Driver Module
-------------------

The motor driver module is a low heat generation one and small packaged
motor drive.

.. image:: media/image124.jpeg
   :width: 400
   :align: center

1. **Power and motor control port**: includes pins for supplying the
   chip and the motors and controlling the motors' direction.

2. **PWM input for the motors**: PWM signal input for adjusting the
   speed of the two motors.

3. **Motor output port**: output port for two motors.

USB Webcam 
----------

.. image:: media/image28.jpeg
   :width: 300
   :align: center

This camera supports a wide angle of 120°, which provides a wide and
clear vision, thus giving better experience when you're using it on the
PiCar-V.

SunFounder SF006C Servo
-----------------------

.. image:: media/image125.png
   :width: 300
   :align: center

Clutch gear digital servo with a DC core motor inside, After a certain
load, the steering gear reducer will automatically clutch and protect
the product from damage and normal load.

Function of the Performance:

=============================== ============ ============
Item                            V = 4.8V     V = 6.0V
Consumption Current\* (No Load) ≦50mA        ≦60mA
Stall Current                   ≦550mA       ≦650mA
Rated Torque                    ≥0.6 kgf·cm  ≥0.7 kgf·cm
Max. Torque                     ≥1.4 kgf.cm  ≥1.6 kgf.cm
No Load Speed                   ≦0.14sec/60° ≦0.12sec/60°
=============================== ============ ============

DC Gear Motor
-------------

.. image:: media/image126.jpeg
   :width: 300
   :align: center

It's a DC motor with a speed reducing gear train. See the parameters
below:

.. image:: media/DC_Gear_Motor.png
   :align: center

