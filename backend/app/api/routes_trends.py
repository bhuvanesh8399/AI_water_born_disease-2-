from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.models import District, DistrictDailyMetric, DistrictProfile, HistoricalAlert
from app.db.session import get_db
from app.services.risk_engine import RiskInputs, compute_risk

router = APIRouter()


def _avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


@router.get("/trends")
def trends(
    district_id: str = Query(..., min_length=1),
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    district = db.get(District, district_id)
    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    profile = db.get(DistrictProfile, district_id)
    if not profile:
        raise HTTPException(status_code=404, detail="District profile not found")

    metrics = (
        db.query(DistrictDailyMetric)
        .filter(DistrictDailyMetric.district_id == district_id)
        .order_by(DistrictDailyMetric.observed_date.asc())
        .all()
    )
    if not metrics:
        return {
            "district_id": district_id,
            "district_name": district.district_name,
            "days": days,
            "points": [],
        }

    historical_alert_dates = [
        item.alert_date
        for item in db.query(HistoricalAlert)
        .filter(HistoricalAlert.district_id == district_id)
        .order_by(HistoricalAlert.alert_date.asc())
        .all()
    ]

    points = []
    for index, metric in enumerate(metrics):
        recent_window = metrics[max(0, index - 6) : index + 1]
        previous_window = metrics[max(0, index - 13) : max(0, index - 6)]

        avg_confirmed_7d = _avg([float(item.total_confirmed_cases) for item in recent_window])
        avg_confirmed_prev_7d = _avg([float(item.total_confirmed_cases) for item in previous_window]) or avg_confirmed_7d
        avg_contamination_7d = _avg([item.avg_water_contamination_level for item in recent_window])
        avg_rainfall_7d = _avg([item.avg_rainfall_mm for item in recent_window])

        recent_alert_count = sum(
            1 for alert_date in historical_alert_dates if 0 <= (metric.observed_date - alert_date).days <= 30
        )

        risk = compute_risk(
            RiskInputs(
                confirmed_cases_latest=metric.total_confirmed_cases,
                avg_confirmed_cases_7d=avg_confirmed_7d,
                avg_confirmed_cases_prev_7d=avg_confirmed_prev_7d,
                contamination_7d=avg_contamination_7d,
                rainfall_7d=avg_rainfall_7d,
                vulnerability_index=profile.vulnerability_index,
                recent_alert_count=recent_alert_count,
                water_quality_index=profile.water_quality_index,
                sanitation_score=profile.sanitation_score,
                healthcare_access_score=profile.healthcare_access_score,
            )
        )

        points.append(
            {
                "date": metric.observed_date.isoformat(),
                "zone_count": metric.zone_count,
                "suspected_cases": metric.total_suspected_cases,
                "confirmed_cases": metric.total_confirmed_cases,
                "avg_rainfall_mm": round(metric.avg_rainfall_mm, 2),
                "avg_temperature_c": round(metric.avg_temperature_c, 2),
                "avg_water_contamination_level": round(metric.avg_water_contamination_level, 3),
                "risk_score": risk.score,
                "risk_level": risk.risk_level,
                "recent_alert_count": recent_alert_count,
            }
        )

    points = points[-days:]

    return {
        "district_id": district_id,
        "district_name": district.district_name,
        "days": days,
        "points": points,
    }
