
import tempfile
import subprocess

_CODE_DIR_ = "/home/pi/video_car_kit"

MJPG_STREAMER_PATH = "mjpg_streamer"
INPUT_PATH = "input_uvc.so"
OUTPUT_PATH = "output_http.so -w /usr/local/www"

stream_cmd = '%s -i "%s" -o "%s" &' % (MJPG_STREAMER_PATH, INPUT_PATH, OUTPUT_PATH)

def run_command(cmd):
	with tempfile.TemporaryFile() as f:
		try:
			subprocess.call(cmd, shell=True, stdout=f, stderr=f)
			f.seek(0)
			output = f.read()
		except:
			pass
	return output

def on():
	run_command(stream_cmd)

def get_host():
	return run_command('hostname -I')