#!/usr/bin/env python
'''
**********************************************************************
* Filename    : stream.py
* Description : A streamer module base on mjpg_streamer
* Author      : xxx
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : xxx    xxxx-xx-xx    New release
*               xxx    xxxx-xx-xx    xxxxxxxx
**********************************************************************
'''
import tempfile
import subprocess
import os

_CODE_DIR_ = os.path.join(os.path.dirname(__file__), '..', '..', ',,')

MJPG_STREAMER_PATH = "mjpg_streamer"
INPUT_PATH = "/usr/local/lib/mjpg-streamer/input_uvc.so"
OUTPUT_PATH = "/usr/local/lib/mjpg-streamer/output_http.so -w /var/www/mjpeg_streamer"

dev_files = os.listdir('/dev')
video_files = sorted([f for f in dev_files if 'video' in f])
if not video_files:
   raise IOError("Camera is not connected correctly")
stream_cmd = '%s -i "%s -d /dev/%s" -o "%s" &' % (MJPG_STREAMER_PATH, INPUT_PATH, video_files[0], OUTPUT_PATH)

def run_command(cmd):
	with tempfile.TemporaryFile() as f:
		subprocess.call(cmd, shell=True, stdout=f, stderr=f)
		f.seek(0)
		output = f.read()
	return output

def start():
	files = os.listdir('/dev')
	print(stream_cmd)
	video_files = [f for f in files if 'video' in f]
	if not video_files:
		raise IOError("Camera is not connected correctly")
	run_command(stream_cmd)

def get_host():
	return run_command('hostname -I')

def stop():
	pid = run_command('ps -A | grep mjpg_streamer | grep -v "grep" | head -n 1')
	if pid == '':
		return False
	else:
		run_command('sudo kill %s' % pid)
		return True

def restart():
	stop()
	start()
	return True

def test():
	run_command(stream_cmd[:-2])

if __name__ == "__main__":
	test()
