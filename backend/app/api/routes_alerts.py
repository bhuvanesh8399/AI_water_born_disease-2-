from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_write_access
from app.db.models import Alert
from app.db.session import get_db

router = APIRouter()


@router.get("/alerts")
def list_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.score.desc(), Alert.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "district_id": item.district_id,
            "district_name": item.district.district_name,
            "prediction_id": item.prediction_id,
            "title": item.title,
            "message": item.message,
            "score": item.score,
            "severity": item.severity,
            "status": item.status,
            "snapshot_date": item.snapshot_date.isoformat(),
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }
        for item in alerts
    ]


@router.patch("/alerts/{alert_id}")
def update_alert(alert_id: int, _: dict = Depends(require_write_access), db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        return {"detail": f"Alert {alert_id} not found"}
    alert.status = "resolved" if alert.status == "active" else "active"
    db.commit()
    db.refresh(alert)
    return {
        "detail": f"Alert {alert_id} updated",
        "id": alert.id,
        "status": alert.status,
    }
