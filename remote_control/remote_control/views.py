import os
import time
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .driver import camera
from picar import back_wheels, front_wheels
import picar

_BASE_DIR = Path(__file__).resolve().parent
_DB_FILE = str(_BASE_DIR / "driver" / "config")

# Valid actions for the run and cali endpoints.
_RUN_ACTIONS = {
    "bwready", "forward", "backward", "stop",
    "fwready", "fwleft", "fwright", "fwstraight",
    "camready", "camleft", "camright", "camup", "camdown",
}

_CALI_ACTIONS = {
    "camcali", "camcaliup", "camcalidown", "camcalileft", "camcaliright", "camcaliok",
    "fwcali", "fwcalileft", "fwcaliright", "fwcaliok",
    "bwcali", "bwcalileft", "bwcaliright", "bwcaliok",
}

# Hardware state — initialized lazily on first use.
_is_setup = False
fw = bw = cam = None
SPEED = 60
bw_status = 0
fw_angle = 90


def _setup():
    global fw, bw, cam, SPEED, bw_status, _is_setup
    if _is_setup:
        return
    picar.setup()
    fw = front_wheels.Front_Wheels(debug=False, db=_DB_FILE)
    bw = back_wheels.Back_Wheels(debug=False, db=_DB_FILE)
    cam = camera.Camera(debug=False, db=_DB_FILE)
    cam.ready()
    bw.ready()
    fw.ready()
    SPEED = 60
    bw_status = 0
    _is_setup = True

    # Start the video stream in a separate process.
    from .picar_v_video_stream import Vilib
    Vilib.camera_start()


def _ensure_setup():
    if not _is_setup:
        _setup()


# --- Page views (GET, render HTML) ---

@ensure_csrf_cookie
@require_GET
def home(request):
    return render(request, "base.html")


@ensure_csrf_cookie
@require_GET
def run_page(request):
    _ensure_setup()
    stream_host = os.environ.get("STREAM_HOST", request.get_host().split(":")[0])
    stream_port = os.environ.get("STREAM_PORT", "8765")
    return render(request, "run.html", {
        "stream_host": stream_host,
        "stream_port": stream_port,
    })


@ensure_csrf_cookie
@require_GET
def cali_page(request):
    _ensure_setup()
    return render(request, "cali.html")


# --- API views (POST, return JSON) ---

@csrf_exempt
@require_POST
def run_action(request):
    global SPEED, bw_status, fw_angle
    _ensure_setup()

    action = request.POST.get("action", "")

    # Handle fwturn:<angle> specially.
    if action.startswith("fwturn:"):
        try:
            angle = int(action.split(":")[1])
            angle = max(45, min(135, angle))
            fw.turn(angle)
            fw_angle = angle
            return JsonResponse({"ok": True})
        except (ValueError, IndexError):
            return JsonResponse({"error": "invalid angle"}, status=400)

    if action not in _RUN_ACTIONS:
        return JsonResponse({"error": "invalid action"}, status=400)

    # Back wheels
    if action == "bwready":
        bw.ready()
        bw_status = 0
    elif action == "forward":
        bw.speed = SPEED
        bw.forward()
        bw_status = 1
    elif action == "backward":
        bw.speed = SPEED
        bw.backward()
        bw_status = -1
    elif action == "stop":
        bw.stop()
        bw_status = 0

    # Front wheels
    elif action == "fwready":
        fw.ready()
        fw_angle = 90
    elif action == "fwleft":
        fw.turn_left()
        fw_angle = 45
    elif action == "fwright":
        fw.turn_right()
        fw_angle = 135
    elif action == "fwstraight":
        fw.turn_straight()
        fw_angle = 90

    # Camera
    elif action == "camready":
        cam.ready()
    elif action == "camleft":
        cam.turn_left(40)
    elif action == "camright":
        cam.turn_right(40)
    elif action == "camup":
        cam.turn_up(20)
    elif action == "camdown":
        cam.turn_down(20)

    return JsonResponse({"ok": True})


@csrf_exempt
@require_POST
def set_speed(request):
    global SPEED, bw_status
    _ensure_setup()

    try:
        speed = int(request.POST.get("speed", 0))
    except (ValueError, TypeError):
        return JsonResponse({"error": "invalid speed"}, status=400)

    SPEED = max(0, min(100, speed))
    if bw_status != 0:
        bw.speed = SPEED

    return JsonResponse({"ok": True, "speed": SPEED})


@require_POST
def cali_action(request):
    _ensure_setup()

    action = request.POST.get("action", "")
    if action not in _CALI_ACTIONS:
        return JsonResponse({"error": "invalid action"}, status=400)

    # Camera calibration
    if action == "camcali":
        cam.calibration()
    elif action == "camcaliup":
        cam.cali_up()
    elif action == "camcalidown":
        cam.cali_down()
    elif action == "camcalileft":
        cam.cali_left()
    elif action == "camcaliright":
        cam.cali_right()
    elif action == "camcaliok":
        cam.cali_ok()

    # Front wheel calibration
    elif action == "fwcali":
        fw.calibration()
    elif action == "fwcalileft":
        fw.cali_left()
    elif action == "fwcaliright":
        fw.cali_right()
    elif action == "fwcaliok":
        fw.cali_ok()

    # Back wheel calibration
    elif action == "bwcali":
        bw.calibration()
    elif action == "bwcalileft":
        bw.cali_left()
    elif action == "bwcaliright":
        bw.cali_right()
    elif action == "bwcaliok":
        bw.cali_ok()

    return JsonResponse({"ok": True})


@csrf_exempt
@require_GET
def vehicle_state(request):
    _ensure_setup()
    return JsonResponse({
        "speed": SPEED,
        "drive": bw_status,
        "steer_angle": fw_angle,
        "cam_pan": cam.current_pan,
        "cam_tilt": cam.current_tilt,
    })


@csrf_exempt
@require_GET
def telemetry_view(request):
    _ensure_setup()
    from . import telemetry as telem
    sys_info = telem.get_system_info()
    net_info = telem.get_network_info()
    return JsonResponse({
        "vehicle": {
            "speed": SPEED,
            "drive": bw_status,
            "steer_angle": fw_angle,
            "cam_pan": cam.current_pan,
            "cam_tilt": cam.current_tilt,
            "cam_pan_offset": cam.pan_offset,
            "cam_tilt_offset": cam.tilt_offset,
            "steer_offset": fw.turning_offset,
        },
        "system": sys_info,
        "network": net_info,
        "hardware": {
            "i2c_devices": telem.get_i2c_devices(),
            "pwm_frequency_hz": 60,
            "servo_channels": {"steer": 0, "cam_pan": 1, "cam_tilt": 2},
            "motor_channels": {"left": 4, "right": 5},
            "motor_gpio": {"a": 17, "b": 27},
        },
        "stream": {
            "active": telem.is_stream_alive(),
            "resolution": "320x240",
            "port": 8765,
            "fps": telem.get_stream_fps(),
        },
        "timestamp": time.time(),
    })


@require_GET
def health_check(request):
    return HttpResponse("OK")
