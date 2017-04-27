# coding=utf-8
#from __future__ import unicode_literals

from picar.SunFounder_PCA9685.Servo import Servo
from picar.SunFounder_PCA9685.PCA9685 import PWM
from picar import front_wheels
from picar import back_wheels
from picar import filedb
from picar import ADC
import picar
import time
from blockext import *
import RPi.GPIO as GPIO
import ball_tracker
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class SunFounder_PiCar_S:
    digital_channel_dic = {"20":20, "16":16, "12":12, "26":26, "19":19, "13":13, "6":6, "5":5}
    def __init__(self):
        self.adc  = ADC(0x48)
        self.fw   = front_wheels.Front_Wheels(db='config')
        self.bw   = back_wheels.Back_Wheels(db='config')
        self.db   = filedb.fileDB(db='config')
        self.turning_offset = int(self.fw.db.get('turning_offset', default_value=0))
        self.pan_offset     = int(self.fw.db.get('pan_offset',     default_value=0))
        self.tilt_offset    = int(self.fw.db.get('tilt_offset',    default_value=0))
        self.pan  = Servo(1)
        self.tilt = Servo(2)

        self.fw.turning_max = 45
        picar.setup()
        GPIO.setmode(GPIO.BCM)

        self.blob_x = 0
        self.blob_y = 0
        self.blob_r = 0

    # === Calibrations =======================================================
    @command("[PiCar-V] Calibrate Front wheels with %n")    # Calibrate front
    def cali_front_wheels(self, offset=0):
        offset = int(offset)
        if offset < -1024:
            offset = -1024
        elif offset > 1024:
            offset = 1024
        #print("offset type: %s"%type(offset))
        self.fw.turning_offset = offset
        print("[PiCar-V] Calibrate Front wheels %s"%(offset))

    @command("[PiCar-V] %m.motor Motor %m.isisnt reversed") # Calibrate motor
    def set_motor_reversed(self, motor, ISISNT="is"):
        if ISISNT == "is":
            value = 1
        elif ISISNT == "is not":
            value = 0
        if motor == "left":
            self.db.set('forward_A', value)
            self.bw.left_wheel.offset = value
        elif motor == "right":
            self.db.set('forward_B', value)
            self.bw.right_wheel.offset = value
        print("[PiCar-V] Motor %s %s reversed"%(motor,ISISNT))
        time.sleep(0.1)

    @command("[PiCar-V] Calibrate Pan with %n")             # Calibrate Pan
    def cali_pan(self, value="0"):
        value = int(value)
        if value < -1024:
            value = -1024
        elif value > 1024:
            value = 1024

        self.pan.offset = value
        self.pan.write(90)

        self.db.set('pan_offset', value)
        print("[PiCar-V] Calibrate Pan %s"%(value))

    @command("[PiCar-V] Calibrate Tilt with %n")            # Calibrate Tilt
    def cali_tilt(self, value="0"):
        value = int(value)
        if value < -1024:
            value = -1024
        elif value > 1024:
            value = 1024

        self.tilt.offset = value
        self.tilt.write(90)

        self.db.set('tilt_offset', value)
        print("[PiCar-V] Calibrate Tilt %s"%(value))

   # === Car & Motor ========================================================
    @command("[PiCar-V] Turn Front wheels %m.turning")              # set Front wheels
    def set_front_wheels(self, turning="straight"):
        if turning == "straight":
            self.fw.turn_straight()
        else:
            if turning == "left":
                self.fw.turn_left()
            elif turning == "right":
                self.fw.turn_right()
            else:
                self.fw.turn(int(turning))

        print("[PiCar-V] Turn Front wheels %s"%(turning))

    @command("[PiCar-V] Set Rear wheels %m.direction at speed %n")  # set Rear wheels
    def set_rear_wheels(self, direction="forward", speed="0"):
        if direction == "forward":
            self.bw.forward()
        elif direction == "backward":
            self.bw.backward()
        speed = int(speed)
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100
        print("[PiCar-V] Set Rear wheels %s at speed %d"%(direction, speed))
        self.bw.speed = speed

    @command("[PiCar-V] Stop")                                      # Stop
    def stop(self):
        print("[PiCar-V] Stop")
        self.fw.ready()
        self.bw.stop()

    # === Digital Ports ====================================================
    @command("[PiCar-V] Set digital channel %m.digital_channel %m.GPIO_state")
    def output_digital_port(self, channel="20", IO_state="HIGH"):  # digital output
        channel = self.digital_channel_dic[channel]
        GPIO.setup(channel, GPIO.OUT)
        if(IO_state == "HIGH"):
            cmd = GPIO.output(channel, GPIO.HIGH)
        else:
            cmd = GPIO.output(channel, GPIO.LOW)
        print ("Set GPIO %s state to %s")%(channel, IO_state)

    @reporter("[PiCar-V] Digital channel %m.digital_channel")      # digital input
    def read_digital_port(self, channel="20"):
        channel = self.digital_channel_dic[channel]
        GPIO.setup(channel, GPIO.IN)
        result = GPIO.input(channel)
        print("Read GPIO %s, state: %s" )%(channel, result)
        return result

    # === ADC ================================================================
    @reporter("[PiCar-V] Analog channel %m.analog_channel ")       # analog input
    def get_analog(self, analog_channel="A0"):
        if analog_channel == "A0":
            value = self.adc.A0
        elif analog_channel == "A1":
            value = self.adc.A1
        elif analog_channel == "A2":
            value = self.adc.A2
        elif analog_channel == "A3":
            value = self.adc.A3
        elif analog_channel == "A4":
            value = self.adc.A4
        print("[PiCar-V] Get Analog channel %s: %d"%(analog_channel,value))
        return value

    # === Servo & PWM ========================================================
    @command("[PiCar-V] Turn Servo %d.pwm_channel to %n degree")   # set Servo
    def set_servo(self, servo="0", angle="90"):
        print("set Servo begin")

        angle = int(angle)
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        self.servo = Servo(int(servo))
        cmd = self.servo.write(angle)
        print("[PiCar-V] Set Servo %s to %d degree"%(servo, angle))

    @command("[PiCar-V] Set PWM channel %d.pwm_channel to %n")     # set PWM
    def set_pwm(self, channel="0", value=2048):
        print("set pwm begin")

        value = int(value)
        if value < 0:
            value = 0
        elif value > 4095:
            value = 4095

        self.pwm = PWM(int(channel))
        cmd = self.pwm.write(value)
        print("[PiCar-V] Set PWM channel %s to %d"%(pwm, value))

    # === Pan_ ===================================================
    @command("[PiCar-V] Set Pan to %n degree")         # Set Pan
    def set_pan(self, angle="90"):
        print("set Pan begin")
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        cmd = self.pan.write(angle)
        print("[PiCar-V] Set Pan to %d degree"%(angle))

    # === Tilt ===================================================
    @command("[PiCar-V] Set Tilt to %n degree")        # Set Tilt
    def set_tilt(self, angle="90"):
        print("set Servo begin")
        if angle < 60:
            angle = 60
        elif angle > 180:
            angle = 180

        cmd = self.tilt.write(angle)
        print("[PiCar-V] Set Tilt to %d degree"%(angle))

    # === Tilt ===================================================
    @command("[PiCar-V] Find red blob")        # Set Tilt
    def find_bolb(self):
        print("Find red blob begin")
        (self.blob_x, self.blob_y), self.blob_r = ball_tracker.find_blob()
        if self.blob_r == -1:
            self.blob_x = (ball_tracker.SCREEN_WIDTH/2)
            self.blob_y = (ball_tracker.SCREEN_HIGHT/2)
        self.blob_x = -((ball_tracker.SCREEN_WIDTH/2) - self.blob_x)
        self.blob_y = (ball_tracker.SCREEN_HIGHT/2) - self.blob_y
        print("x: %s, y: %s, r: %s"%(self.blob_x, self.blob_y, self.blob_r))
        print("[PiCar-V] Find red blob")

    # === ADC ================================================================
    @reporter("[PiCar-V] Blob %m.blob_state")       # analog input
    def get_blob(self, state="x"):
        if state == "x":
            value = self.blob_x
        elif state == "y":
            value = self.blob_y
        elif state == "r":
            value = self.blob_r
        print("[PiCar-V] Blob %s.blob_state: %d"%(state, value))
        return value

descriptor = Descriptor(
    name = "PiCar-V",
    host = "0.0.0.0",
    port = 8080,
    category = "motion",
    blocks = get_decorated_blocks_from_class(SunFounder_PiCar_S),
    menus = dict(
        direction = ["forward", "backward"],
        turning = ["left", "straight", "right"],
        motor = ["left","right"],
        analog_channel = ["A0", "A1", "A2", "A3"],
        digital_channel = ["B20", "B16", "B12", "B26", "B19", "B13", "B6", "B5"],
        pwm_channel = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        isisnt = ["is", "is not"],
        GPIO_state = ["HIGH", "LOW"],
        blob_state = ['x', 'y', 'r'],
    ),
)

extension = Extension(SunFounder_PiCar_S, descriptor)

if __name__ == "__main__":
    extension.run_forever(debug=True)

