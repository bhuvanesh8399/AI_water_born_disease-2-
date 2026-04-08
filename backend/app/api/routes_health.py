from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Alert, District, DistrictDailyMetric, HistoricalAlert, Observation, Prediction
from app.db.session import get_db

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    return {
        "status": "ok",
        "district_count": db.query(District).count(),
        "observation_count": db.query(Observation).count(),
        "daily_metric_count": db.query(DistrictDailyMetric).count(),
        "historical_alert_count": db.query(HistoricalAlert).count(),
        "prediction_count": db.query(Prediction).count(),
        "active_alert_count": db.query(Alert).filter(Alert.status == "active").count(),
    }
