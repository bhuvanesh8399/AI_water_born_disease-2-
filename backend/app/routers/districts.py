from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.query_service import district_detail, district_trends, list_districts

router = APIRouter(tags=["districts"])


@router.get("/api/districts")
def api_list_districts(db: Session = Depends(get_db)):
    return list_districts(db)


@router.get("/api/districts/{district_id}")
def api_district_detail(district_id: str, db: Session = Depends(get_db)):
    payload = district_detail(db, district_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="District not found")
    return payload


@router.get("/api/dashboard/trends/{district_id}")
def api_district_trends(
    district_id: str,
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
):
    return district_trends(db, district_id=district_id, days=days)
