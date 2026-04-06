"""PiCar-V Relay Server — proxies commands from the public internet to the Pi."""

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

from .auth import create_token, verify_token, verify_token_query
from .config import settings
from . import proxy as pi_proxy
from . import mock

app = FastAPI(title="PiCar-V Relay")

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.get("/")
async def index():
    return FileResponse(_STATIC_DIR / "index.html")


class AuthRequest(BaseModel):
    password: str


@app.post("/api/auth/")
async def auth(body: AuthRequest):
    if body.password != settings.auth_password:
        return JSONResponse({"error": "invalid password"}, status_code=401)
    token = create_token()
    return {"token": token}


@app.get("/api/health/")
async def health():
    if settings.mock_mode:
        return {"relay": "ok", "vehicle": "mock", "mock_mode": True}
    return pi_proxy.get_health_info()


# ---------------------------------------------------------------------------
# Authenticated proxy routes
# ---------------------------------------------------------------------------

@app.get("/api/state/")
async def state(_=Depends(verify_token)):
    if settings.mock_mode:
        return mock.get_state()
    return await pi_proxy.proxy_get("/api/state/")


@app.get("/api/telemetry/")
async def telemetry(_=Depends(verify_token)):
    if settings.mock_mode:
        return mock.get_telemetry()
    return await pi_proxy.proxy_get("/api/telemetry/")


@app.post("/api/action/")
async def action(request: Request, _=Depends(verify_token)):
    body = await request.json()
    action_name = body.get("action", "")
    if settings.mock_mode:
        return mock.handle_action(action_name)
    return await pi_proxy.proxy_post("/api/action/", {"action": action_name})


@app.post("/api/speed/")
async def speed(request: Request, _=Depends(verify_token)):
    body = await request.json()
    speed_val = body.get("speed", 0)
    if settings.mock_mode:
        return mock.handle_speed(int(speed_val))
    return await pi_proxy.proxy_post("/api/speed/", {"speed": speed_val})


@app.post("/api/ping/")
async def ping(_=Depends(verify_token)):
    """Noop ACK — sends a ping to the car and waits for a response."""
    if settings.mock_mode:
        return mock.handle_ping()
    return await pi_proxy.proxy_post("/api/ping/", {})


@app.get("/api/stream/")
async def stream(_=Depends(verify_token_query)):
    if settings.mock_mode:
        return JSONResponse(
            {"error": "stream not available in mock mode"},
            status_code=503,
        )
    return StreamingResponse(
        pi_proxy.proxy_stream("/mjpg"),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
