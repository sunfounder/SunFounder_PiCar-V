"""HTTP proxy to the PiCar-V Django app over Tailscale."""

import asyncio
import time
from collections import deque

import httpx

from .config import settings

# Connection state tracking
last_successful_contact: float = 0.0
_latency_window: deque[float] = deque(maxlen=20)

# Shared httpx client — created lazily
_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        proxy = settings.proxy_url or None
        _client = httpx.AsyncClient(
            proxy=proxy,
            timeout=httpx.Timeout(connect=2.0, read=3.0, write=3.0, pool=5.0),
        )
    return _client


def _pi_url(port: int, path: str) -> str:
    return f"http://{settings.picar_host}:{port}{path}"


async def proxy_get(path: str, port: int | None = None) -> dict:
    """Proxy a GET request to the Pi and return the JSON response."""
    global last_successful_contact
    port = port or settings.picar_port
    client = _get_client()
    t0 = time.monotonic()
    try:
        resp = await client.get(_pi_url(port, path))
        dt = (time.monotonic() - t0) * 1000
        _latency_window.append(dt)
        last_successful_contact = time.time()
        return resp.json()
    except (httpx.ConnectError, httpx.TimeoutException, httpx.ReadError) as e:
        return _unreachable_response(str(e))


async def proxy_post(path: str, data: dict, port: int | None = None) -> dict:
    """Proxy a POST request (form-encoded) to the Pi and return JSON."""
    global last_successful_contact
    port = port or settings.picar_port
    client = _get_client()
    t0 = time.monotonic()
    try:
        resp = await client.post(_pi_url(port, path), data=data)
        dt = (time.monotonic() - t0) * 1000
        _latency_window.append(dt)
        last_successful_contact = time.time()
        return resp.json()
    except (httpx.ConnectError, httpx.TimeoutException, httpx.ReadError) as e:
        return _unreachable_response(str(e))


async def proxy_stream(path: str, port: int | None = None):
    """Yield chunks from the Pi's MJPEG stream. On failure, yield a
    'SIGNAL LOST' placeholder frame and retry."""
    port = port or settings.picar_stream_port
    client = _get_client()
    url = _pi_url(port, path)

    while True:
        try:
            async with client.stream("GET", url) as resp:
                async for chunk in resp.aiter_bytes(chunk_size=4096):
                    yield chunk
        except (httpx.ConnectError, httpx.TimeoutException, httpx.ReadError, httpx.StreamClosed):
            # Yield a placeholder frame
            yield _signal_lost_frame()
            await asyncio.sleep(2)
        except GeneratorExit:
            return


def _unreachable_response(detail: str = "") -> dict:
    return {
        "error": "vehicle_unreachable",
        "message": f"Cannot reach PiCar-V: {detail}",
        "last_seen": last_successful_contact,
    }


def get_health_info() -> dict:
    latencies = list(_latency_window)
    return {
        "relay": "ok",
        "vehicle": "reachable" if last_successful_contact > time.time() - 10 else "unreachable",
        "vehicle_last_seen": last_successful_contact,
        "latency_ms": round(latencies[-1], 1) if latencies else None,
        "latency_avg_ms": round(sum(latencies) / len(latencies), 1) if latencies else None,
        "latency_max_ms": round(max(latencies), 1) if latencies else None,
    }


def _signal_lost_frame() -> bytes:
    """Generate a minimal MJPEG frame with 'SIGNAL LOST' text.

    We create a tiny valid JPEG using raw bytes — a 8x8 black JPEG with
    the boundary markers expected by the MJPEG stream.
    """
    # Minimal 8x8 black JPEG
    # For a proper implementation we'd use Pillow, but this keeps deps minimal.
    # This is a valid 8x8 all-black JPEG.
    black_jpeg = (
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
        b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
        b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342'
        b'\xff\xc0\x00\x0b\x08\x00\x08\x00\x08\x01\x01\x11\x00'
        b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
        b'\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04'
        b'\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa'
        b'\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n'
        b'\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz'
        b'\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99'
        b'\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7'
        b'\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5'
        b'\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1'
        b'\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
        b'\xff\xda\x00\x08\x01\x01\x00\x00?\x00T\xdb\xa8\xa1\xc2\xd3\x8bO'
        b'\xff\xd9'
    )
    return (
        b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + black_jpeg + b'\r\n'
    )
