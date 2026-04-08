from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_write_access
from app.db import get_db
from app.models import Alert, District
from app.services.pipeline_service import json_loads_safe

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/alerts")
def api_alerts(db: Session = Depends(get_db)):
    rows = (
        db.query(Alert, District.district_name)
        .join(District, District.district_id == Alert.district_id)
        .order_by(Alert.predicted_date.desc(), Alert.created_at.desc())
        .all()
    )
    return [
        {
            "id": alert.id,
            "district_id": alert.district_id,
            "district_name": district_name,
            "predicted_date": str(alert.predicted_date),
            "severity": alert.severity,
            "status": alert.status,
            "title": alert.title,
            "message": alert.message,
            "confidence_score": alert.confidence_score,
            "owner_role": alert.owner_role,
            "reasons": json_loads_safe(alert.reasons_json),
            "recommended_actions": json_loads_safe(alert.recommended_actions_json),
        }
        for alert, district_name in rows
    ]


@router.patch("/alerts/{alert_id}")
def api_update_alert(
    alert_id: int,
    payload: dict = Body(default_factory=dict),
    _: dict = Depends(require_write_access),
    db: Session = Depends(get_db),
):
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found",
        )

    next_status = str(payload.get("status") or "RESOLVED").upper()
    alert.status = next_status
    db.commit()
    db.refresh(alert)

    return {
        "id": alert.id,
        "status": alert.status,
        "detail": f"Alert {alert_id} updated",
    }
