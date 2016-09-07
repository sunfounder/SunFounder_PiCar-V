#!/usr/bin/env python

import sys, time, http.client
from PyQt5 import QtCore, uic, QtWidgets  # pyqt4 -> pyqt5 , QtGui -> QtWidgets
import icons_rc
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from urllib.request import urlopen
import requests

login_screen     = "login_screen.ui" 
running_screen   = "running_screen.ui"
setting_screen   = "setting_screen.ui"
calibrate_screen = "calibrate_screen.ui"

Ui_Login_screen, QtBaseClass     = uic.loadUiType(login_screen)
Ui_Running_screen, QtBaseClass   = uic.loadUiType(running_screen)
Ui_Setting_screen, QtBaseClass   = uic.loadUiType(setting_screen)
Ui_Calibrate_screen, QtBaseClass = uic.loadUiType(calibrate_screen)
 
MAX_SPEED = 100
MIN_SPEED = 40
SPEED_LEVEL_1 = MIN_SPEED
SPEED_LEVEL_2 = (MAX_SPEED - MIN_SPEED) / 4 * 1 + MIN_SPEED
SPEED_LEVEL_3 = (MAX_SPEED - MIN_SPEED) / 4 * 2 + MIN_SPEED
SPEED_LEVEL_4 = (MAX_SPEED - MIN_SPEED) / 4 * 3 + MIN_SPEED
SPEED_LEVEL_5 = MAX_SPEED
SPEED = [0, SPEED_LEVEL_1, SPEED_LEVEL_2, SPEED_LEVEL_3, SPEED_LEVEL_4, SPEED_LEVEL_5]

HOST      = '192.168.0.133'
PORT 	  = '8000'
autologin = True

BASE_URL = 'http://' + HOST + ':'+ PORT + '/'

def reflash_url():
	global BASE_URL
	BASE_URL = 'http://' + HOST + ':'+ PORT + '/'

class LoginScreen(QtWidgets.QDialog, Ui_Login_screen):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)	
		Ui_Login_screen.__init__(self)
		self.setupUi(self)

		if autologin == True:
			self.lEd_host.setText(HOST)
			self.label_Error.setText("")
			self.pBtn_checkbox.setStyleSheet("border-image: url(./images/check2.png);")
		else:
			self.lEd_host.setText("")
			self.label_Error.setText("")
			self.pBtn_checkbox.setStyleSheet("border-image: url(./images/uncheck1.png);")

		self.pBtn_checkbox.clicked.connect(self.on_pBtn_checkbox_clicked)

	def on_pBtn_login_clicked(self):
		global HOST,PORT
		# check whether the length of input host and port is allowable
		if 7<len(self.lEd_host.text())<16 :
			HOST = self.lEd_host.text()
			PORT = self.lEd_port.text()
			reflash_url()
			self.label_Error.setText("Connecting....")
			
			# check whethe server is connected
			if connection_ok() == True: # request respon 'OK', connected
				if autologin == True:	# autologin checked，record HOST
					HOST = self.lEd_host.text()
				else:
					self.lEd_host.setText("")
					self.label_Error.setText("")
				self.label_Error.setText("")
				login1.close()
				running1.start_stream()
				running1.show()
				return True
			else:
				self.label_Error.setText("Failed to connect")
				return False

		else:
			self.label_Error.setText("Host or port not correct")
			return False
		print ("on_pBtn_login_clicked", HOST,PORT,autologin,"\n")
	
	def on_pBtn_login_pressed(self):
		self.pBtn_login.setStyleSheet("border-image: url(./images/login_button_pressed.png);color: rgb(255, 255, 255);")
	def on_pBtn_login_released(self):
		self.pBtn_login.setStyleSheet("border-image: url(./images/login_button_unpressed.png);color: rgb(255, 255, 255);")	
	def on_pBtn_checkbox_clicked(self):
		global autologin
		autologin = not autologin
		if autologin == True:
			self.pBtn_checkbox.setStyleSheet("border-image: url(./images/check2.png);")
		else:
			self.pBtn_checkbox.setStyleSheet("border-image: url(./images/uncheck1.png);")
		print ("on_pBtn_checkbox_clicked", HOST,autologin)

class RunningScreen(QtWidgets.QMainWindow, Ui_Running_screen):
	TIMEOUT = 50
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)	
		Ui_Running_screen.__init__(self)
		self.setupUi(self)

		self.speed_level = 0
		self.level_btn_show(self.speed_level)
		self.btn_back.setStyleSheet("border-image: url(./images/back_unpressed.png);")
		self.btn_setting.setStyleSheet("border-image: url(./images/settings_unpressed.png);")
	
	def start_stream(self):
		self.queryImage = QueryImage(HOST)
		self.timer = QTimer(timeout=self.reflash_frame) # Qt timer，time out, run reflash_frame()
		self.timer.start(RunningScreen.TIMEOUT)
		run_action('fwready')
		run_action('bwready')
		run_action('camready')
	
	def stop_stream(self):
		self.timer.stop()

	def transToPixmap(self):
		data = self.queryImage.queryImage()
		if not data:
			return None
		pixmap = QPixmap()
		pixmap.loadFromData(data)
		return pixmap

	def reflash_frame(self):
		pixmap = self.transToPixmap()
		if pixmap:
			self.label_snapshot.setPixmap(pixmap)
		else :
			print ("frame lost")
	
	def level_btn_show(self,speed_level):
		self.level1.setStyleSheet("border-image: url(./images/speed_level_1_unpressed.png);")
		self.level2.setStyleSheet("border-image: url(./images/speed_level_2_unpressed.png);")
		self.level3.setStyleSheet("border-image: url(./images/speed_level_3_unpressed.png);")
		self.level4.setStyleSheet("border-image: url(./images/speed_level_4_unpressed.png);")
		self.level5.setStyleSheet("border-image: url(./images/speed_level_5_unpressed.png);")
		if   speed_level == 1:
			self.level1.setStyleSheet("border-image: url(./images/speed_level_1_pressed.png);")
		elif speed_level == 2:
			self.level2.setStyleSheet("border-image: url(./images/speed_level_2_pressed.png);")
		elif speed_level == 3:
			self.level3.setStyleSheet("border-image: url(./images/speed_level_3_pressed.png);")	
		elif speed_level == 4:
			self.level4.setStyleSheet("border-image: url(./images/speed_level_4_pressed.png);")	
		elif speed_level == 5:
			self.level5.setStyleSheet("border-image: url(./images/speed_level_5_pressed.png);")	

	def set_speed_level(self, speed):
		run_speed(speed)

	def keyPressEvent(self, event):
		key_press = event.key()

		if not event.isAutoRepeat():
			if key_press == Qt.Key_Up:
				run_action('camup')
			elif key_press == Qt.Key_Right:
				run_action('camright')
			elif key_press == Qt.Key_Down:
				run_action('camdown')
			elif key_press == Qt.Key_Left:
				run_action('camleft')
			elif key_press == Qt.Key_W:
				run_action('forward')
			elif key_press == Qt.Key_A:
				run_action('fwleft')
			elif key_press == Qt.Key_S:
				run_action('backward')
			elif key_press == Qt.Key_D:
				run_action('fwright')

	def keyReleaseEvent(self, event):
		key_release = event.key()
		if not event.isAutoRepeat():
			if key_release == Qt.Key_Up:
				run_action('camready')
			elif key_release == Qt.Key_Right:
				run_action('camready')
			elif key_release == Qt.Key_Down:
				run_action('camready')
			elif key_release == Qt.Key_Left:
				run_action('camready')
			elif key_release == Qt.Key_W:
				run_action('stop')
			elif key_release == Qt.Key_A:
				run_action('fwstraight')
			elif key_release == Qt.Key_S:
				run_action('stop')
			elif key_release == Qt.Key_D:
				run_action('fwstraight')

	def on_level1_clicked(self):
		self.speed_level = 1
		self.level_btn_show(self.speed_level)
		self.set_speed_level('20')
	
	def on_level2_clicked(self):
		self.speed_level = 2
		self.level_btn_show(self.speed_level)
		self.set_speed_level('40')
	
	def on_level3_clicked(self):
		self.speed_level = 3
		self.level_btn_show(self.speed_level)
		self.set_speed_level('60')

	def on_level4_clicked(self):
		self.speed_level = 4
		self.level_btn_show(self.speed_level)
		self.set_speed_level('80')	

	def on_level5_clicked(self):
		self.speed_level = 5
		self.level_btn_show(self.speed_level)
		self.set_speed_level('100')

	def on_btn_back_pressed(self):
		self.btn_back.setStyleSheet("border-image: url(./images/back_pressed.png);")
	def on_btn_back_released(self):
		self.btn_back.setStyleSheet("border-image: url(./images/back_unpressed.png);")
	def on_btn_back_clicked(self):
		self.close()
		self.stop_stream()
		login1.show()

	def on_btn_setting_pressed(self):
		self.btn_setting.setStyleSheet("border-image: url(./images/settings_pressed.png);")
	def on_btn_setting_released(self):
		self.btn_setting.setStyleSheet("border-image: url(./images/settings_unpressed.png);")
	def on_btn_setting_clicked(self):
		self.btn_back.setStyleSheet("border-image: url(./images/back_unpressed.png);")
		self.close()
		setting1.show()
		
class SettingScreen(QtWidgets.QMainWindow, Ui_Setting_screen):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)	
		Ui_Setting_screen.__init__(self)
		self.setupUi(self)

		self.btn_back.setStyleSheet("border-image: url(./images/back_unpressed.png);")

	def on_btn_camera_cali_pressed(self):
		self.btn_camera_cali.setStyleSheet("border-image: url(./images/camera_cali_pressed.png);")
	def on_btn_camera_cali_released(self):
		self.btn_camera_cali.setStyleSheet("border-image: url(./images/camera_cali_unpressed.png);")
	def on_btn_camera_cali_clicked(self):
		calibrate1.calibration_show(1)

	def on_btn_fw_cali_pressed(self):
		self.btn_fw_cali.setStyleSheet("border-image: url(./images/fw_cali_pressed.png);")
	def on_btn_fw_cali_released(self):
		self.btn_fw_cali.setStyleSheet("border-image: url(./images/fw_cali_unpressed.png);")
	def on_btn_fw_cali_clicked(self):
		calibrate1.calibration_show(2)

	def on_btn_bw_cali_pressed(self):
		self.btn_bw_cali.setStyleSheet("border-image: url(./images/bw_cali_pressed.png);")
	def on_btn_bw_cali_released(self):
		self.btn_bw_cali.setStyleSheet("border-image: url(./images/bw_cali_unpressed.png);")
	def on_btn_bw_cali_clicked(self):
		calibrate1.calibration_show(3)

	def on_btn_back_pressed(self):
		self.btn_back.setStyleSheet("border-image: url(./images/back_pressed.png);")
	def on_btn_back_released(self):
		self.btn_back.setStyleSheet("border-image: url(./images/back_unpressed.png);")
	def on_btn_back_clicked(self):
		self.close()
		running1.show()

class CalibrateScreen(QtWidgets.QMainWindow, Ui_Calibrate_screen):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)	
		Ui_Calibrate_screen.__init__(self)
		self.setupUi(self)
		self.calibration_status = 0

		self.btn_ok.setStyleSheet("border-image: url(./images/ok_unpressed.png);")
		self.btn_cancle.setStyleSheet("border-image: url(./images/cancle_unpressed.png);")

	def calibration_show(self, calibration_status):
		self.calibration_status = calibration_status
		if self.calibration_status == 1:
			cali_action('camcali')
			self.label_pic.setStyleSheet("image: url(./images/camera_cali.JPG);")
			self.label_Cali_Info.setText("Camera")
			self.label_Info_1.setText("Calibrate the camera to the position like above.")
			self.label_Info_2.setText("Use Keyboard Up, Down, Left, Right or W, A, S, D.")
		if self.calibration_status == 2:
			cali_action('fwcali')
			self.label_pic.setStyleSheet("image: url(./images/front_wheel_cali.JPG);")
			self.label_Cali_Info.setText("Front Wheels")
			self.label_Info_1.setText("Calibrate front wheels to the position like above.")
			self.label_Info_2.setText("Use Keyboard Left, Right or A, D.")
		if self.calibration_status == 3:
			cali_action('bwcali')
			self.label_pic.setStyleSheet("image: url(./images/back_wheel_cali.JPG);")
			self.label_Cali_Info.setText("Back Wheels")
			self.label_Info_1.setText("Calibrate back wheels to the direction like above.")
			self.label_Info_2.setText("Use Keyboard Left, Right or A, D, to reverse motor")
		self.show()

	def keyPressEvent(self, event):
		key_press = event.key()

		if key_press in (Qt.Key_Up, Qt.Key_W):    	# UP
			if   self.calibration_status == 1:
				cali_action('camcaliup')
			elif self.calibration_status == 2:
				pass
			elif self.calibration_status == 3:
				pass
		elif key_press in (Qt.Key_Right, Qt.Key_D):	# RIGHT
			if   self.calibration_status == 1:
				cali_action('camcaliright')
			elif self.calibration_status == 2:
				cali_action('fwcaliright')
			elif self.calibration_status == 3:
				cali_action('bwcaliright')
		elif key_press in (Qt.Key_Down, Qt.Key_S):	# DOWN
			if   self.calibration_status == 1:
				cali_action('camcalidown')
			elif self.calibration_status == 2:
				pass
			elif self.calibration_status == 3:
				pass
		elif key_press in (Qt.Key_Left, Qt.Key_A):	# LEFT
			if   self.calibration_status == 1:
				cali_action('camcalileft')
			elif self.calibration_status == 2:
				cali_action('fwcalileft')
			elif self.calibration_status == 3:
				cali_action('bwcalileft')
		elif key_press == Qt.Key_Escape:			# ESC
			run_action('stop')
			self.close()			

	def on_btn_ok_pressed(self):
		self.btn_ok.setStyleSheet("border-image: url(./images/ok_pressed.png);")
	def on_btn_ok_released(self):
		self.btn_ok.setStyleSheet("border-image: url(./images/ok_unpressed.png);")
	def on_btn_ok_clicked(self):
		if   self.calibration_status == 1:
			cali_action('camcaliok')
		elif self.calibration_status == 2:
			cali_action('fwcaliok')
		elif self.calibration_status == 3:
			cali_action('bwcaliok')
		self.close()		

	def on_btn_cancle_pressed(self):
		self.btn_cancle.setStyleSheet("border-image: url(./images/cancle_pressed.png);")
	def on_btn_cancle_released(self):
		self.btn_cancle.setStyleSheet("border-image: url(./images/cancle_unpressed.png);")
	def on_btn_cancle_clicked(self):
		if   self.calibration_status == 1:
			cali_action('camready')
		elif self.calibration_status == 2:
			cali_action('fwready')
		elif self.calibration_status == 3:
			cali_action('bwready')
		self.close()		

class QueryImage:
	def __init__(self, host, port=8080, argv="/?action=snapshot"):
		self.host = host
		self.port = port
		self.argv = argv
	
	def queryImage(self):
		http_data = http.client.HTTPConnection(self.host, self.port)
		http_data.putrequest('GET', self.argv)
		http_data.putheader('Host', self.host)
		http_data.putheader('User-agent', 'python-http.client')
		http_data.putheader('Content-type', 'image/jpeg')
		http_data.endheaders()
		returnmsg = http_data.getresponse()

		return returnmsg.read()

def connection_ok():
	cmd = 'connection_test'
	url = BASE_URL + cmd
	print('url: %s'% url)
	try:
		r=requests.get(url)
		if r.text == 'OK':
			return True
	except:
		return False

def run_action(cmd):
	url = BASE_URL + 'run/?action=' + cmd
	print('url: %s'% url)
	requests.get(url)

def run_speed(speed):
	url = BASE_URL + 'run/?speed=' + speed
	print('url: %s'% url)
	requests.get(url)

def cali_action(cmd):
	url = BASE_URL + 'cali/?action=' + cmd
	print('url: %s'% url)
	requests.get(url)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	
	login1 = LoginScreen()
	running1 = RunningScreen()	
	setting1   = SettingScreen()
	calibrate1 = CalibrateScreen()

	login1.show()

	print ("All done")
	sys.exit(app.exec_())
		
