from sqlalchemy.orm import Session

from app.db.models import District, DistrictDailyMetric, HistoricalAlert
from app.services.risk_engine import RiskInputs, compute_risk


def build_trends(db: Session, district_id: int, days: int) -> dict:
    public_id = f"D{district_id:03d}"
    district = db.get(District, public_id)
    if district is None:
        return {"district_id": district_id, "district_name": "Unknown", "points": []}

    metrics = (
        db.query(DistrictDailyMetric)
        .filter(DistrictDailyMetric.district_id == public_id)
        .order_by(DistrictDailyMetric.observed_date.desc())
        .limit(days)
        .all()
    )
    metrics = list(reversed(metrics))
    historical_alerts = (
        db.query(HistoricalAlert)
        .filter(HistoricalAlert.district_id == public_id)
        .all()
    )

    points = []
    for index, item in enumerate(metrics):
        recent_window = metrics[max(0, index - 6) : index + 1]
        previous_window = metrics[max(0, index - 13) : max(0, index - 6)]
        avg_confirmed_7d = sum(metric.total_confirmed_cases for metric in recent_window) / len(recent_window)
        avg_confirmed_prev_7d = (
            sum(metric.total_confirmed_cases for metric in previous_window) / len(previous_window)
            if previous_window
            else avg_confirmed_7d
        )
        recent_alert_count = sum(
            1 for alert in historical_alerts if 0 <= (item.observed_date - alert.alert_date).days <= 30
        )
        result = compute_risk(
            RiskInputs(
                confirmed_cases_latest=item.total_confirmed_cases,
                avg_confirmed_cases_7d=avg_confirmed_7d,
                avg_confirmed_cases_prev_7d=avg_confirmed_prev_7d,
                contamination_7d=item.avg_water_contamination_level,
                rainfall_7d=item.avg_rainfall_mm,
                vulnerability_index=district.profile.vulnerability_index,
                recent_alert_count=recent_alert_count,
                water_quality_index=district.profile.water_quality_index,
                sanitation_score=district.profile.sanitation_score,
                healthcare_access_score=district.profile.healthcare_access_score,
            )
        )
        points.append(
            {
                "date": item.observed_date.isoformat(),
                "score": result.score,
                "risk_level": result.risk_level,
            }
        )
    return {
        "district_id": district_id,
        "district_name": district.district_name,
        "points": points,
    }
