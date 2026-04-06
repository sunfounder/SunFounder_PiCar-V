import time

import jwt
from fastapi import Depends, HTTPException, Query, Request

from .config import settings

_ALGORITHM = "HS256"


def create_token() -> str:
    exp = time.time() + settings.jwt_expiry_hours * 3600
    return jwt.encode({"exp": exp}, settings.jwt_secret, algorithm=_ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_token(request: Request) -> dict:
    """FastAPI dependency — extract and validate JWT from Authorization header."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return _decode_token(auth[7:])
    raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")


def verify_token_query(token: str = Query(None)) -> dict:
    """FastAPI dependency — extract JWT from query param (for img src etc.)."""
    if not token:
        raise HTTPException(status_code=401, detail="Missing token query parameter")
    return _decode_token(token)
