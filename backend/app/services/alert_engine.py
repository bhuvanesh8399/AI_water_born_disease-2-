from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Alert, Prediction


def regenerate_current_alerts(db: Session) -> None:
    predictions = (
        db.query(Prediction)
        .filter(Prediction.risk_level == "high")
        .order_by(Prediction.score.desc())
        .all()
    )
    active_alerts = {
        item.district_id: item for item in db.query(Alert).filter(Alert.status == "active").all()
    }
    high_risk_districts = {item.district_id for item in predictions}

    for district_id, alert in active_alerts.items():
        if district_id not in high_risk_districts:
            alert.status = "resolved"
            alert.updated_at = datetime.utcnow()

    for prediction in predictions:
        district = prediction.district
        existing = active_alerts.get(prediction.district_id)
        if existing is None:
            db.add(
                Alert(
                    district_id=district.district_id,
                    prediction_id=prediction.id,
                    snapshot_date=prediction.observed_date,
                    title=f"High risk in {district.district_name}",
                    message=prediction.explanation,
                    score=prediction.score,
                    severity="high",
                    status="active",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )
            continue

        existing.prediction_id = prediction.id
        existing.snapshot_date = prediction.observed_date
        existing.title = f"High risk in {district.district_name}"
        existing.message = prediction.explanation
        existing.score = prediction.score
        existing.severity = "high"
        existing.status = "active"
        existing.updated_at = datetime.utcnow()
    db.commit()
