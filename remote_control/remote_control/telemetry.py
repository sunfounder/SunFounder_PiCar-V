"""System telemetry gathering for the Raspberry Pi.

Reads from /proc and /sys — no external dependencies needed.
All functions return safe defaults if the expected files don't exist
(e.g. when running on macOS for development).
"""

import os
import socket
import subprocess
import time

# ---------------------------------------------------------------------------
# CPU
# ---------------------------------------------------------------------------

_prev_cpu = None
_prev_cpu_time = 0.0


def read_cpu_temp():
    """Read CPU temperature in degrees Celsius."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read().strip()) / 1000.0, 1)
    except (OSError, ValueError):
        return None


def read_cpu_percent():
    """Compute CPU usage % as delta since last call."""
    global _prev_cpu, _prev_cpu_time
    try:
        with open("/proc/stat") as f:
            parts = f.readline().split()
        # user, nice, system, idle, iowait, irq, softirq, steal
        vals = list(map(int, parts[1:9]))
        idle = vals[3] + vals[4]
        total = sum(vals)
    except (OSError, ValueError, IndexError):
        return None

    if _prev_cpu is None:
        _prev_cpu = (idle, total)
        _prev_cpu_time = time.monotonic()
        return 0.0

    d_idle = idle - _prev_cpu[0]
    d_total = total - _prev_cpu[1]
    _prev_cpu = (idle, total)
    _prev_cpu_time = time.monotonic()

    if d_total == 0:
        return 0.0
    return round((1.0 - d_idle / d_total) * 100, 1)


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------

def read_mem_info():
    """Return dict with mem_total_mb, mem_available_mb, mem_used_percent."""
    info = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    info["mem_total_mb"] = int(line.split()[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    info["mem_available_mb"] = int(line.split()[1]) // 1024
                if len(info) == 2:
                    break
    except OSError:
        return {"mem_total_mb": None, "mem_available_mb": None, "mem_used_percent": None}

    total = info.get("mem_total_mb")
    avail = info.get("mem_available_mb")
    if total and avail:
        info["mem_used_percent"] = round((1 - avail / total) * 100, 1)
    else:
        info["mem_used_percent"] = None
    return info


# ---------------------------------------------------------------------------
# Disk
# ---------------------------------------------------------------------------

def read_disk_info():
    """Return dict with disk_total_gb, disk_free_gb, disk_used_percent."""
    try:
        st = os.statvfs("/")
        total = st.f_blocks * st.f_frsize
        free = st.f_bavail * st.f_frsize
        total_gb = round(total / (1024 ** 3), 1)
        free_gb = round(free / (1024 ** 3), 1)
        used_pct = round((1 - free / total) * 100, 1) if total else 0
        return {"disk_total_gb": total_gb, "disk_free_gb": free_gb, "disk_used_percent": used_pct}
    except OSError:
        return {"disk_total_gb": None, "disk_free_gb": None, "disk_used_percent": None}


# ---------------------------------------------------------------------------
# Uptime
# ---------------------------------------------------------------------------

def read_uptime():
    """Return system uptime in seconds."""
    try:
        with open("/proc/uptime") as f:
            return round(float(f.read().split()[0]), 1)
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------

def read_net_stats():
    """Parse /proc/net/dev and return per-interface rx/tx bytes."""
    result = {}
    try:
        with open("/proc/net/dev") as f:
            for line in f:
                if ":" not in line:
                    continue
                iface, data = line.split(":", 1)
                iface = iface.strip()
                parts = data.split()
                result[iface] = {
                    "rx_bytes": int(parts[0]),
                    "tx_bytes": int(parts[8]),
                }
    except (OSError, ValueError, IndexError):
        pass
    return result


def read_wifi_rssi():
    """Read WiFi signal level in dBm from /proc/net/wireless."""
    try:
        with open("/proc/net/wireless") as f:
            lines = f.readlines()
        for line in lines[2:]:  # skip header lines
            parts = line.split()
            # signal level is the 3rd field (index 3), may have trailing '.'
            level = float(parts[3].rstrip("."))
            return level
    except (OSError, ValueError, IndexError):
        return None


_tailscale_ip_cache = None


def read_tailscale_ip():
    """Get the Tailscale IPv4 address (cached after first call)."""
    global _tailscale_ip_cache
    if _tailscale_ip_cache is not None:
        return _tailscale_ip_cache
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            _tailscale_ip_cache = result.stdout.strip()
            return _tailscale_ip_cache
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


# ---------------------------------------------------------------------------
# Battery (PCF8591 ADC on Robot HAT — I2C bus 1, address 0x48)
# Channel 4 is wired to battery via 20K/10K voltage divider (3:1 ratio).
# ---------------------------------------------------------------------------

_PCF8591_ADDR = 0x48
_I2C_BUS = 1
_smbus = None


def _get_smbus():
    """Lazy-init smbus to avoid import errors on dev machines."""
    global _smbus
    if _smbus is None:
        try:
            import smbus2
            _smbus = smbus2.SMBus(_I2C_BUS)
        except (ImportError, OSError):
            return None
    return _smbus


def read_battery_voltage():
    """Read battery voltage from PCF8591 ADC.

    The Robot HAT routes battery through a 20K/10K voltage divider,
    so actual voltage = ADC voltage * 3.
    PCF8591 is 8-bit (0-255), reference voltage 3.3V.

    We scan all 4 channels (AIN0-AIN3) and return the highest reading,
    since the battery channel varies across Robot HAT revisions.
    """
    bus = _get_smbus()
    if bus is None:
        return None
    best = 0.0
    for channel in range(4):
        try:
            # Control byte: 0x40 | channel = DAC enable + channel select
            # First read after switching channel is stale — read twice.
            bus.write_byte(_PCF8591_ADDR, 0x40 | channel)
            bus.read_byte(_PCF8591_ADDR)  # discard stale
            raw = bus.read_byte(_PCF8591_ADDR)
            adc_voltage = raw / 255.0 * 3.3
            voltage = adc_voltage * 3.0
            if voltage > best:
                best = voltage
        except (OSError, IOError):
            continue
    return round(best, 2) if best > 0 else None


def read_power_info():
    """Determine power source and throttling state.

    Returns dict with:
      - source: "battery", "usb", or "unknown"
      - voltage: battery voltage (from ADC) or None
      - under_voltage: True if Pi reports under-voltage (vcgencmd bit 0)
      - throttled_raw: raw hex throttled value
    """
    voltage = read_battery_voltage()

    # Battery connected if ADC reads > 2V (anything meaningful)
    if voltage is not None and voltage > 2.0:
        source = "battery"
    elif voltage is not None:
        source = "usb"
    else:
        source = "unknown"

    # Check Pi firmware throttling flags
    under_voltage = False
    throttled_raw = None
    try:
        result = subprocess.run(
            ["vcgencmd", "get_throttled"],
            capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0:
            # Output: "throttled=0x0"
            hex_str = result.stdout.strip().split("=")[-1]
            throttled_raw = hex_str
            flags = int(hex_str, 16)
            under_voltage = bool(flags & 0x1)  # bit 0: under-voltage now
    except (OSError, subprocess.TimeoutExpired, ValueError):
        pass

    return {
        "source": source,
        "voltage": voltage,
        "under_voltage": under_voltage,
        "throttled_raw": throttled_raw,
    }


# ---------------------------------------------------------------------------
# I2C
# ---------------------------------------------------------------------------

_i2c_cache = None
_i2c_cache_time = 0
_I2C_CACHE_TTL = 60  # seconds


def get_i2c_devices():
    """Detect I2C devices on bus 1 via smbus2 scan (cached for 60s)."""
    global _i2c_cache, _i2c_cache_time
    now = time.time()
    if _i2c_cache is not None and (now - _i2c_cache_time) < _I2C_CACHE_TTL:
        return _i2c_cache

    bus = _get_smbus()
    if bus is None:
        return []

    devices = []
    for addr in range(0x03, 0x78):
        try:
            bus.read_byte(addr)
            devices.append("0x%02x" % addr)
        except (OSError, IOError):
            continue

    _i2c_cache = devices
    _i2c_cache_time = now
    return devices


# ---------------------------------------------------------------------------
# Stream
# ---------------------------------------------------------------------------

def is_stream_alive():
    """Check if the video stream Flask process is running."""
    import multiprocessing
    for proc in multiprocessing.active_children():
        if proc.name == "worker 1":
            return proc.is_alive()
    return False


# Shared frame counter — set by picar_v_video_stream if available.
_frame_count_ref = None
_last_fps_check = 0.0
_last_frame_count = 0
_current_fps = 0.0


def set_frame_counter(shared_value):
    """Called by picar_v_video_stream to register the shared frame counter."""
    global _frame_count_ref
    _frame_count_ref = shared_value


def get_stream_fps():
    """Compute approximate stream FPS from the shared frame counter."""
    global _last_fps_check, _last_frame_count, _current_fps
    if _frame_count_ref is None:
        return None
    try:
        now = time.monotonic()
        count = _frame_count_ref.value
        dt = now - _last_fps_check
        if dt >= 1.0:
            _current_fps = round((count - _last_frame_count) / dt, 1)
            _last_frame_count = count
            _last_fps_check = now
        return _current_fps
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Aggregated helpers
# ---------------------------------------------------------------------------

def get_system_info():
    """Return a dict of all system-level telemetry."""
    mem = read_mem_info()
    disk = read_disk_info()
    try:
        load = list(os.getloadavg())
    except OSError:
        load = None
    return {
        "cpu_temp_c": read_cpu_temp(),
        "cpu_percent": read_cpu_percent(),
        "load_avg": load,
        **mem,
        **disk,
        "uptime_seconds": read_uptime(),
        "hostname": socket.gethostname(),
    }


def get_network_info():
    """Return a dict of all network telemetry."""
    return {
        "interfaces": read_net_stats(),
        "wifi_rssi_dbm": read_wifi_rssi(),
        "tailscale_ip": read_tailscale_ip(),
    }
