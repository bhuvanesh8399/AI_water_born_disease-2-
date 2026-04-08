from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Alert, Prediction
from app.db.session import get_db

router = APIRouter()


@router.get("/heatmap")
def heatmap(db: Session = Depends(get_db)):
    rows = (
        db.query(Prediction)
        .order_by(Prediction.district_id.asc(), Prediction.observed_date.desc(), Prediction.created_at.desc())
        .all()
    )
    latest: dict[str, Prediction] = {}
    for row in rows:
        latest.setdefault(row.district_id, row)

    active_alert_districts = {
        item.district_id for item in db.query(Alert).filter(Alert.status == "active").all()
    }

    points = []
    for prediction in sorted(latest.values(), key=lambda row: row.score, reverse=True):
        district = prediction.district
        points.append(
            {
                "district_id": district.district_id,
                "district_name": district.district_name,
                "state": district.state,
                "latitude": district.latitude,
                "longitude": district.longitude,
                "population": district.population,
                "risk_score": prediction.score,
                "risk_level": prediction.risk_level,
                "observed_date": prediction.observed_date.isoformat(),
                "active_alert": district.district_id in active_alert_districts,
                "confirmed_cases_latest": prediction.confirmed_cases_latest,
                "contamination_7d": prediction.contamination_7d,
                "vulnerability_index": prediction.vulnerability_index,
            }
        )
    return {"count": len(points), "points": points}
