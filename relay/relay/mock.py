"""Mock responses for local development when the Pi car is not available."""

import math
import random
import time

_start_time = time.time()
_mock_state = {
    "speed": 60,
    "drive": 0,
    "steer_angle": 90,
    "cam_pan": 90,
    "cam_tilt": 90,
}


def handle_action(action: str) -> dict:
    if action.startswith("fwturn:"):
        try:
            angle = int(action.split(":")[1])
            _mock_state["steer_angle"] = max(45, min(135, angle))
        except (ValueError, IndexError):
            return {"error": "invalid angle"}
    elif action == "forward":
        _mock_state["drive"] = 1
    elif action == "backward":
        _mock_state["drive"] = -1
    elif action in ("stop", "bwready"):
        _mock_state["drive"] = 0
    elif action == "fwleft":
        _mock_state["steer_angle"] = 45
    elif action == "fwright":
        _mock_state["steer_angle"] = 135
    elif action in ("fwstraight", "fwready"):
        _mock_state["steer_angle"] = 90
    elif action == "camready":
        _mock_state["cam_pan"] = 90
        _mock_state["cam_tilt"] = 90
    elif action == "camleft":
        _mock_state["cam_pan"] = min(180, _mock_state["cam_pan"] + 40)
    elif action == "camright":
        _mock_state["cam_pan"] = max(0, _mock_state["cam_pan"] - 40)
    elif action == "camup":
        _mock_state["cam_tilt"] = min(180, _mock_state["cam_tilt"] + 20)
    elif action == "camdown":
        _mock_state["cam_tilt"] = max(0, _mock_state["cam_tilt"] - 20)
    return {"ok": True}


def handle_speed(speed: int) -> dict:
    _mock_state["speed"] = max(0, min(100, speed))
    return {"ok": True, "speed": _mock_state["speed"]}


def get_state() -> dict:
    return dict(_mock_state)


def get_telemetry() -> dict:
    t = time.time()
    uptime = t - _start_time + 86400 * 3  # pretend 3 days uptime
    cpu_temp = 42.0 + 5 * math.sin(t / 30)
    return {
        "vehicle": {
            **_mock_state,
            "cam_pan_offset": 0,
            "cam_tilt_offset": 0,
            "steer_offset": 0,
        },
        "system": {
            "cpu_temp_c": round(cpu_temp, 1),
            "cpu_percent": round(random.uniform(15, 45), 1),
            "load_avg": [
                round(random.uniform(0.5, 1.5), 2),
                round(random.uniform(0.8, 1.2), 2),
                round(random.uniform(0.7, 1.0), 2),
            ],
            "mem_total_mb": 1024,
            "mem_available_mb": round(random.uniform(400, 600)),
            "mem_used_percent": round(random.uniform(40, 60), 1),
            "disk_total_gb": 29.7,
            "disk_free_gb": round(random.uniform(15, 20), 1),
            "disk_used_percent": round(random.uniform(30, 50), 1),
            "uptime_seconds": round(uptime, 1),
            "hostname": "picar-v-mock",
        },
        "network": {
            "interfaces": {
                "wlan0": {
                    "rx_bytes": int(1.2e9 + random.randint(0, 1000000)),
                    "tx_bytes": int(8.4e8 + random.randint(0, 1000000)),
                },
                "tailscale0": {
                    "rx_bytes": int(5e7 + random.randint(0, 100000)),
                    "tx_bytes": int(3e7 + random.randint(0, 100000)),
                },
            },
            "wifi_rssi_dbm": round(random.uniform(-55, -45), 0),
            "tailscale_ip": "100.64.0.42",
        },
        "hardware": {
            "i2c_devices": ["0x40"],
            "pwm_frequency_hz": 60,
            "servo_channels": {"steer": 0, "cam_pan": 1, "cam_tilt": 2},
            "motor_channels": {"left": 4, "right": 5},
            "motor_gpio": {"a": 17, "b": 27},
        },
        "stream": {
            "active": True,
            "resolution": "320x240",
            "port": 8765,
            "fps": round(random.uniform(25, 30), 1),
        },
        "timestamp": t,
    }
