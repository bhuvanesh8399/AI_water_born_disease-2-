from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.constants import WRITE_PROTECTED_MESSAGE

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(subject: str, role: str = "admin", expires_minutes: Optional[int] = None) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])


def get_current_actor(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, Any]:
    settings = get_settings()
    if not settings.auth_enabled:
        return {"email": "demo@example.com", "role": "viewer", "demo": True}
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = decode_access_token(credentials.credentials)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return {
        "email": payload.get("sub", ""),
        "role": payload.get("role", "viewer"),
        "demo": False,
    }


def require_write_access(actor: dict[str, Any] = Depends(get_current_actor)) -> dict[str, Any]:
    settings = get_settings()
    if not settings.auth_enabled and settings.read_only_demo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=WRITE_PROTECTED_MESSAGE)
    if actor.get("role") not in {"admin", "analyst"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return actor
