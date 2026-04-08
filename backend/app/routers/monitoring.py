from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.query_service import monitoring_status

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/status")
def api_monitoring_status(db: Session = Depends(get_db)):
    return monitoring_status(db)
