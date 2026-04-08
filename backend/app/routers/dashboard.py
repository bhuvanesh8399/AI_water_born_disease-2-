from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.query_service import dashboard_alerts, dashboard_hotspots, dashboard_summary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def api_dashboard_summary(db: Session = Depends(get_db)):
    return dashboard_summary(db)


@router.get("/hotspots")
def api_dashboard_hotspots(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return dashboard_hotspots(db, limit=limit)


@router.get("/alerts")
def api_dashboard_alerts(
    status: str = Query("ACTIVE"),
    db: Session = Depends(get_db),
):
    return dashboard_alerts(db, status=status)
