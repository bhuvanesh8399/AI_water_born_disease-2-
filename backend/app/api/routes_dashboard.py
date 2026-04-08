from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Alert, Prediction
from app.db.session import get_db

router = APIRouter()


def _latest_predictions(db: Session) -> list[Prediction]:
    rows = (
        db.query(Prediction)
        .order_by(Prediction.district_id.asc(), Prediction.observed_date.desc(), Prediction.created_at.desc())
        .all()
    )
    latest: dict[str, Prediction] = {}
    for row in rows:
        latest.setdefault(row.district_id, row)
    return list(latest.values())


def _serialize_hotspot(prediction: Prediction) -> dict:
    district = prediction.district
    return {
        "district_id": district.district_id,
        "district_name": district.district_name,
        "state": district.state,
        "state_name": district.state,
        "latitude": district.latitude,
        "longitude": district.longitude,
        "risk_score": prediction.score,
        "score": prediction.score,
        "risk_level": prediction.risk_level,
        "zone_type": None,
        "observed_date": prediction.observed_date.isoformat(),
        "confirmed_cases_latest": prediction.confirmed_cases_latest,
        "contamination_7d": prediction.contamination_7d,
        "recent_alert_count": prediction.recent_alert_count,
        "explanation": prediction.explanation,
    }


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    latest_predictions = _latest_predictions(db)
    active_alerts = (
        db.query(Alert)
        .filter(Alert.status == "active")
        .order_by(Alert.score.desc(), Alert.created_at.desc())
        .all()
    )

    high_risk = [item for item in latest_predictions if item.risk_level == "high"]
    medium_risk = [item for item in latest_predictions if item.risk_level == "medium"]
    low_risk = [item for item in latest_predictions if item.risk_level == "low"]

    hotspots = [
        _serialize_hotspot(item)
        for item in sorted(latest_predictions, key=lambda row: row.score, reverse=True)[:10]
    ]

    last_updated: date | None = None
    if latest_predictions:
        last_updated = max(item.observed_date for item in latest_predictions)

    recent_alerts = [
        {
            "id": alert.id,
            "district_id": alert.district_id,
            "district_name": alert.district.district_name,
            "title": alert.title,
            "message": alert.message,
            "score": alert.score,
            "severity": alert.severity,
            "status": alert.status,
            "snapshot_date": alert.snapshot_date.isoformat(),
            "created_at": alert.created_at.isoformat(),
            "updated_at": alert.updated_at.isoformat(),
        }
        for alert in active_alerts[:10]
    ]

    summary = {
        "district_count": len(latest_predictions),
        "total_districts": len(latest_predictions),
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(medium_risk),
        "low_risk_count": len(low_risk),
        "active_alert_count": len(active_alerts),
        "active_alerts": len(active_alerts),
        "last_updated": last_updated.isoformat() if last_updated else None,
        "updated_at": last_updated.isoformat() if last_updated else None,
    }

    return {
        **summary,
        "summary": summary,
        "risk_distribution": {
            "high": len(high_risk),
            "medium": len(medium_risk),
            "low": len(low_risk),
        },
        "hotspots": hotspots,
        "recent_alerts": recent_alerts,
    }


@router.get("/hotspots")
def hotspots(db: Session = Depends(get_db)):
    latest_predictions = _latest_predictions(db)
    return [_serialize_hotspot(item) for item in sorted(latest_predictions, key=lambda row: row.score, reverse=True)]
