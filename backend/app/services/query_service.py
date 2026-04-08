from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    Alert,
    District,
    DistrictDailyMetric,
    DistrictEnrichment,
    DistrictProfile,
    HistoricalAlert,
    ObservationRaw,
    Prediction,
    WeatherObservation,
)
from app.services.pipeline_service import (
    ensure_today_predictions,
    get_latest_metric,
    get_latest_weather,
    json_loads_safe,
    normalize_district_id,
    now_utc,
)


def health_payload(db: Session) -> dict:
    return {
        "status": "ok",
        "database": "connected",
        "districts": db.query(func.count(District.district_id)).scalar() or 0,
        "time": now_utc().isoformat(),
    }


def dashboard_summary(db: Session) -> dict:
    ensure_today_predictions(db)
    today = date.today()
    total_districts = db.query(func.count(District.district_id)).scalar() or 0
    high_risk = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.predicted_date == today, Prediction.risk_level == "HIGH")
        .scalar()
        or 0
    )
    medium_risk = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.predicted_date == today, Prediction.risk_level == "MEDIUM")
        .scalar()
        or 0
    )
    low_risk = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.predicted_date == today, Prediction.risk_level == "LOW")
        .scalar()
        or 0
    )
    active_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.predicted_date == today, Alert.status == "ACTIVE")
        .scalar()
        or 0
    )
    avg_score = (
        db.query(func.avg(Prediction.final_score)).filter(Prediction.predicted_date == today).scalar() or 0.0
    )
    avg_confidence = (
        db.query(func.avg(Prediction.confidence_score))
        .filter(Prediction.predicted_date == today)
        .scalar()
        or 0.0
    )
    return {
        "total_districts": int(total_districts),
        "high_risk": int(high_risk),
        "medium_risk": int(medium_risk),
        "low_risk": int(low_risk),
        "active_alerts": int(active_alerts),
        "average_risk_score": round(float(avg_score), 2),
        "average_confidence_score": round(float(avg_confidence), 2),
        "last_updated": now_utc().isoformat(),
    }


def dashboard_hotspots(db: Session, limit: int = 10) -> list[dict]:
    ensure_today_predictions(db)
    today = date.today()
    rows = (
        db.query(Prediction, District.district_name)
        .join(District, District.district_id == Prediction.district_id)
        .filter(Prediction.predicted_date == today)
        .order_by(Prediction.final_score.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "district_id": pred.district_id,
            "district_name": district_name,
            "final_score": pred.final_score,
            "risk_level": pred.risk_level,
            "confidence_score": pred.confidence_score,
            "rule_score": pred.rule_score,
            "rf_score": pred.rf_score,
            "xgb_score": pred.xgb_score,
            "reasons": json_loads_safe(pred.reasons_json),
        }
        for pred, district_name in rows
    ]


def dashboard_alerts(db: Session, status: str = "ACTIVE") -> list[dict]:
    query = (
        db.query(Alert, District.district_name)
        .join(District, District.district_id == Alert.district_id)
        .order_by(Alert.predicted_date.desc(), Alert.created_at.desc())
    )
    if status.upper() != "ALL":
        query = query.filter(Alert.status == status.upper())

    rows = query.limit(100).all()
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


def list_districts(db: Session) -> list[dict]:
    districts = db.query(District).order_by(District.district_name.asc()).all()
    return [
        {
            "district_id": district.district_id,
            "district_name": district.district_name,
            "state": district.state,
            "population": district.population,
            "latitude": district.latitude,
            "longitude": district.longitude,
        }
        for district in districts
    ]


def district_detail(db: Session, district_id: str) -> dict | None:
    ensure_today_predictions(db)
    district_id = normalize_district_id(district_id)
    district = db.query(District).filter(District.district_id == district_id).first()
    if not district:
        return None

    profile = db.query(DistrictProfile).filter(DistrictProfile.district_id == district_id).first()
    enrich = db.query(DistrictEnrichment).filter(DistrictEnrichment.district_id == district_id).first()
    weather = get_latest_weather(db, district_id)
    metric = get_latest_metric(db, district_id)
    prediction = (
        db.query(Prediction)
        .filter(Prediction.district_id == district_id)
        .order_by(Prediction.predicted_date.desc())
        .first()
    )
    hist_alerts = (
        db.query(HistoricalAlert)
        .filter(HistoricalAlert.district_id == district_id)
        .order_by(HistoricalAlert.alert_date.desc())
        .limit(15)
        .all()
    )

    return {
        "district": {
            "district_id": district.district_id,
            "district_name": district.district_name,
            "state": district.state,
            "population": district.population,
            "latitude": district.latitude,
            "longitude": district.longitude,
        },
        "profile": {
            "water_quality_index": profile.water_quality_index if profile else None,
            "sanitation_score": profile.sanitation_score if profile else None,
            "healthcare_access_score": profile.healthcare_access_score if profile else None,
            "population_density": profile.population_density if profile else None,
            "vulnerability_index": profile.vulnerability_index if profile else None,
        }
        if profile
        else None,
        "enrichment": {
            "population_total": enrich.population_total if enrich else None,
            "population_density": enrich.population_density if enrich else None,
            "rural_population_pct": enrich.rural_population_pct if enrich else None,
            "urban_population_pct": enrich.urban_population_pct if enrich else None,
            "literacy_rate_pct": enrich.literacy_rate_pct if enrich else None,
            "sanitation_coverage_pct": enrich.sanitation_coverage_pct if enrich else None,
            "drinking_water_coverage_pct": enrich.drinking_water_coverage_pct if enrich else None,
            "water_quality_affected_pct": enrich.water_quality_affected_pct if enrich else None,
            "primary_health_centres": enrich.primary_health_centres if enrich else None,
            "total_health_facilities": enrich.total_health_facilities if enrich else None,
            "estimated_hospital_beds": enrich.estimated_hospital_beds if enrich else None,
            "vulnerability_score_raw": enrich.vulnerability_score_raw if enrich else None,
            "vulnerability_level": enrich.vulnerability_level if enrich else None,
            "waterborne_disease_index": enrich.waterborne_disease_index if enrich else None,
            "public_health_risk_score": enrich.public_health_risk_score if enrich else None,
        }
        if enrich
        else None,
        "latest_weather": {
            "date": str(weather.date),
            "rainfall_mm": weather.rainfall_mm,
            "temperature_max_c": weather.temperature_max_c,
            "temperature_min_c": weather.temperature_min_c,
        }
        if weather
        else None,
        "latest_metric": {
            "observed_date": str(metric.observed_date),
            "avg_baseline_water_level": metric.avg_baseline_water_level,
            "avg_drainage_score": metric.avg_drainage_score,
            "sanitation_score": metric.sanitation_score,
            "population_density": metric.population_density,
            "vulnerability_index": metric.vulnerability_index,
            "anomaly_score": metric.anomaly_score,
            "previous_alerts_count": metric.previous_alerts_count,
            "historical_alert_count": metric.historical_alert_count,
        }
        if metric
        else None,
        "latest_prediction": {
            "predicted_date": str(prediction.predicted_date),
            "rule_score": prediction.rule_score,
            "rf_score": prediction.rf_score,
            "xgb_score": prediction.xgb_score,
            "final_score": prediction.final_score,
            "risk_level": prediction.risk_level,
            "confidence_score": prediction.confidence_score,
            "data_completeness": prediction.data_completeness,
            "data_freshness_score": prediction.data_freshness_score,
            "model_agreement_score": prediction.model_agreement_score,
            "reasons": json_loads_safe(prediction.reasons_json),
            "recommended_actions": json_loads_safe(prediction.recommended_actions_json),
            "chosen_model": prediction.chosen_model,
        }
        if prediction
        else None,
        "historical_alerts": [
            {
                "alert_id": alert.alert_id,
                "alert_date": str(alert.alert_date),
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "status": alert.status,
            }
            for alert in hist_alerts
        ],
    }


def district_trends(db: Session, district_id: str, days: int = 30) -> list[dict]:
    district_id = normalize_district_id(district_id)
    since = date.today() - timedelta(days=days)

    preds = (
        db.query(Prediction)
        .filter(Prediction.district_id == district_id, Prediction.predicted_date >= since)
        .order_by(Prediction.predicted_date.asc())
        .all()
    )
    metrics = (
        db.query(DistrictDailyMetric)
        .filter(DistrictDailyMetric.district_id == district_id, DistrictDailyMetric.observed_date >= since)
        .order_by(DistrictDailyMetric.observed_date.asc())
        .all()
    )
    weather_rows = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.district_id == district_id, WeatherObservation.date >= since)
        .order_by(WeatherObservation.date.asc())
        .all()
    )

    pred_map = {str(pred.predicted_date): pred for pred in preds}
    metric_map = {str(row.observed_date): row for row in metrics}
    weather_map = {str(row.date): row for row in weather_rows}
    timeline_dates = sorted(set(pred_map.keys()) | set(metric_map.keys()) | set(weather_map.keys()))

    points = []
    for d in timeline_dates:
        pred = pred_map.get(d)
        metric = metric_map.get(d)
        weather = weather_map.get(d)
        points.append(
            {
                "date": d,
                "final_score": pred.final_score if pred else None,
                "rule_score": pred.rule_score if pred else None,
                "rf_score": pred.rf_score if pred else None,
                "xgb_score": pred.xgb_score if pred else None,
                "risk_level": pred.risk_level if pred else None,
                "anomaly_score": metric.anomaly_score if metric else None,
                "drainage_score": metric.avg_drainage_score if metric else None,
                "rainfall_mm": weather.rainfall_mm if weather else None,
            }
        )
    return points


def monitoring_status(db: Session) -> dict:
    latest_weather_date = db.query(func.max(WeatherObservation.date)).scalar()
    latest_metric_date = db.query(func.max(DistrictDailyMetric.observed_date)).scalar()

    from app.services.pipeline_service import MODEL_CACHE

    return {
        "districts_total": db.query(func.count(District.district_id)).scalar() or 0,
        "profiles_total": db.query(func.count(DistrictProfile.district_id)).scalar() or 0,
        "enrichments_total": db.query(func.count(DistrictEnrichment.district_id)).scalar() or 0,
        "observations_total": db.query(func.count(ObservationRaw.id)).scalar() or 0,
        "metrics_total": db.query(func.count(DistrictDailyMetric.id)).scalar() or 0,
        "historical_alerts_total": db.query(func.count(HistoricalAlert.alert_id)).scalar() or 0,
        "weather_rows_total": db.query(func.count(WeatherObservation.id)).scalar() or 0,
        "predictions_today": (
            db.query(func.count(Prediction.id))
            .filter(Prediction.predicted_date == date.today())
            .scalar()
            or 0
        ),
        "active_alerts_today": (
            db.query(func.count(Alert.id))
            .filter(Alert.predicted_date == date.today(), Alert.status == "ACTIVE")
            .scalar()
            or 0
        ),
        "latest_weather_date": str(latest_weather_date) if latest_weather_date else None,
        "latest_metric_date": str(latest_metric_date) if latest_metric_date else None,
        "rf_model_loaded": MODEL_CACHE["rf"] is not None,
        "xgb_model_loaded": MODEL_CACHE["xgb"] is not None,
        "trained_features": MODEL_CACHE["meta"].get("features", []),
    }
