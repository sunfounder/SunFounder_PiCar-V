from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

picar.setup()
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

if (show_image_enable or draw_circle_enable) and "DISPLAY" not in os.environ:
    print('Warning: Display not found, turn off "show_image_enable" and "draw_circle_enable"')
    show_image_enable   = False
    draw_circle_enable  = False

kernel = np.ones((5,5),np.uint8)
img = cv2.VideoCapture(-1)

if not img.isOpened:
    print("not open")
else:
    print("open")
    
SCREEN_WIDTH = 160
SCREEN_HIGHT = 120
img.set(3,SCREEN_WIDTH)
img.set(4,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
BALL_SIZE_MIN = SCREEN_HIGHT/10
BALL_SIZE_MAX = SCREEN_HIGHT/3

# Filter setting, DONOT CHANGE
hmn = 12
hmx = 37
smn = 96
smx = 255
vmn = 186
vmx = 255

# camera follow mode:
# 0 = step by step(slow, stable), 
# 1 = calculate the step(fast, unstable)
follow_mode = 1

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

SCAN_POS = [[20, TILT_ANGLE_MIN], [50, TILT_ANGLE_MIN], [90, TILT_ANGLE_MIN], [130, TILT_ANGLE_MIN], [160, TILT_ANGLE_MIN], 
            [160, 80], [130, 80], [90, 80], [50, 80], [20, 80]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)

motor_speed = 60

def nothing(x):
    pass

def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 90             # initial angle for tilt
    fw_angle = 90

    scan_count = 0
    print("Begin!")
    while True:
        x = 0             # x initial in the middle
        y = 0             # y initial in the middle
        r = 0             # ball radius initial to 0(no balls if r < ball_size)

        for _ in range(10):
            (tmp_x, tmp_y), tmp_r = find_blob()
            if tmp_r > BALL_SIZE_MIN:
                x = tmp_x
                y = tmp_y
                r = tmp_r
                break

        print(x, y, r)

        # scan:
        if r < BALL_SIZE_MIN:
            bw.stop()
            if scan_enable:
                #bw.stop()
                pan_angle = SCAN_POS[scan_count][0]
                tilt_angle = SCAN_POS[scan_count][1]
                if pan_tilt_enable:
                    pan_servo.write(pan_angle)
                    tilt_servo.write(tilt_angle)
                scan_count += 1
                if scan_count >= len(SCAN_POS):
                    scan_count = 0
            else:
                sleep(0.1)
            
        elif r < BALL_SIZE_MAX:
            if follow_mode == 0:
                if abs(x - CENTER_X) > MIDDLE_TOLERANT:
                    if x < CENTER_X:                              # Ball is on left
                        pan_angle += CAMERA_STEP
                        #print("Left   ", )
                        if pan_angle > PAN_ANGLE_MAX:
                            pan_angle = PAN_ANGLE_MAX
                    else:                                         # Ball is on right
                        pan_angle -= CAMERA_STEP
                        #print("Right  ",)
                        if pan_angle < PAN_ANGLE_MIN:
                            pan_angle = PAN_ANGLE_MIN
                if abs(y - CENTER_Y) > MIDDLE_TOLERANT:
                    if y < CENTER_Y :                             # Ball is on top
                        tilt_angle += CAMERA_STEP
                        #print("Top    " )
                        if tilt_angle > TILT_ANGLE_MAX:
                            tilt_angle = TILT_ANGLE_MAX
                    else:                                         # Ball is on bottom
                        tilt_angle -= CAMERA_STEP
                        #print("Bottom ")
                        if tilt_angle < TILT_ANGLE_MIN:
                            tilt_angle = TILT_ANGLE_MIN
            else:
                delta_x = CENTER_X - x
                delta_y = CENTER_Y - y
                #print("x = %s, delta_x = %s" % (x, delta_x))
                #print("y = %s, delta_y = %s" % (y, delta_y))
                delta_pan = int(float(CAMERA_X_ANGLE) / SCREEN_WIDTH * delta_x)
                #print("delta_pan = %s" % delta_pan)
                pan_angle += delta_pan
                delta_tilt = int(float(CAMERA_Y_ANGLE) / SCREEN_HIGHT * delta_y)
                #print("delta_tilt = %s" % delta_tilt)
                tilt_angle += delta_tilt

                if pan_angle > PAN_ANGLE_MAX:
                    pan_angle = PAN_ANGLE_MAX
                elif pan_angle < PAN_ANGLE_MIN:
                    pan_angle = PAN_ANGLE_MIN
                if tilt_angle > TILT_ANGLE_MAX:
                    tilt_angle = TILT_ANGLE_MAX
                elif tilt_angle < TILT_ANGLE_MIN:
                    tilt_angle = TILT_ANGLE_MIN
            
            if pan_tilt_enable:
                pan_servo.write(pan_angle)
                tilt_servo.write(tilt_angle)
            sleep(0.01)
            fw_angle = 180 - pan_angle
            if fw_angle < FW_ANGLE_MIN or fw_angle > FW_ANGLE_MAX:
                fw_angle = ((180 - fw_angle) - 90)/2 + 90
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    bw.backward()
            else:
                if front_wheels_enable:
                    fw.turn(fw_angle)
                if rear_wheels_enable:
                    bw.speed = motor_speed
                    bw.forward()
        else:
            bw.stop()
        
def destroy():
    bw.stop()
    img.release()

def test():
    fw.turn(90)

def find_blob() :
    radius = 0
    # Load input image
    #_, bgr_image = img.read()
    ret, bgr_image = img.read()
    if ret == False:
        print("Failed to read image")
        
    orig_image = bgr_image

    bgr_image = cv2.medianBlur(bgr_image, 3)
  
    # Convert input image to HSV
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image, keep only the red pixels
    lower_red_hue_range = cv2.inRange(hsv_image, (0, 100, 100), (10, 255, 255))
    upper_red_hue_range = cv2.inRange(hsv_image, (160, 100, 100), (179, 255, 255))
    # Combine the above two images
    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)

    red_hue_image = cv2.GaussianBlur(red_hue_image, (9, 9), 2, 2)

    # Use the Hough transform to detect circles in the combined threshold image
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
 
    # Loop over all detected circles and outline them on the original image
        all_r = np.array([])
    # print("circles: %s"%circles)
        try:
            for i in circles[0,:]:
                # print("i: %s"%i)
                all_r = np.append(all_r, int(round(i[2])))
            closest_ball = all_r.argmax()
            center=(int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1])))
            radius=int(round(circles[0][closest_ball][2]))
            if draw_circle_enable:
                cv2.circle(orig_image, center, radius, (0, 255, 0), 5)
        except IndexError:
            pass
            #print("circles: %s"%circles)

    # Show images
    if show_image_enable:
        cv2.namedWindow("Threshold lower image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold lower image", lower_red_hue_range)
        cv2.namedWindow("Threshold upper image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Threshold upper image", upper_red_hue_range)
        cv2.namedWindow("Combined threshold images", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Combined threshold images", red_hue_image)
        cv2.namedWindow("Detected red circles on the input image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Detected red circles on the input image", orig_image)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        return (0, 0), 0
    if radius > 3:
        return center, radius
    else:
        return (0, 0), 0


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
