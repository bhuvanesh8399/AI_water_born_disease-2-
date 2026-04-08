from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token

router = APIRouter()
settings = get_settings()


@router.post("/login")
def login(payload: dict):
    if not settings.auth_enabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication is disabled")

    email = payload.get("email", "")
    password = payload.get("password", "")
    if email != settings.default_admin_email or password != settings.default_admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": create_access_token(subject=email, role="admin"),
        "token_type": "bearer",
        "email": email,
        "role": "admin",
    }
