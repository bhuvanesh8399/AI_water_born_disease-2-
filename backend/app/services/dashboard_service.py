from sqlalchemy.orm import Session

from app.db.models import District, Prediction


def _public_district_id(value: str) -> int:
    if value.upper().startswith("D"):
        value = value[1:]
    return int(value)


def _latest_predictions(db: Session) -> list[Prediction]:
    return (
        db.query(Prediction)
        .join(District)
        .order_by(Prediction.score.desc(), District.district_name.asc())
        .all()
    )


def build_dashboard_summary(db: Session) -> dict:
    predictions = _latest_predictions(db)
    return {
        "total_districts": db.query(District).count(),
        "high_risk_count": sum(1 for item in predictions if item.risk_level == "high"),
        "medium_risk_count": sum(1 for item in predictions if item.risk_level == "medium"),
        "low_risk_count": sum(1 for item in predictions if item.risk_level == "low"),
        "updated_at": predictions[0].created_at.isoformat() if predictions else None,
        "hotspots": [
            {
                "district_id": _public_district_id(item.district_id),
                "district_name": item.district.district_name,
                "state_name": item.district.state,
                "zone_type": None,
                "latitude": item.district.latitude,
                "longitude": item.district.longitude,
                "score": item.score,
                "risk_level": item.risk_level,
            }
            for item in predictions[:10]
        ],
    }
