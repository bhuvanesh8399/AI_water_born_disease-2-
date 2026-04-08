import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import (
    Alert,
    District,
    DistrictDailyMetric,
    DistrictProfile,
    HistoricalAlert,
    Observation,
    Prediction,
    Setting,
)
from app.services.alert_engine import regenerate_current_alerts
from app.services.risk_engine import RiskInputs, compute_risk
from app.utils.dates import parse_date

settings = get_settings()

REQUIRED_COLUMNS = {
    "district_master.csv": {"district_id", "district_name", "state", "population", "latitude", "longitude"},
    "district_profile.csv": {
        "district_id",
        "water_quality_index",
        "sanitation_score",
        "healthcare_access_score",
        "population_density",
        "vulnerability_index",
    },
    "observations_base.csv": {
        "observation_id",
        "district_id",
        "zone",
        "date",
        "suspected_cases",
        "confirmed_cases",
        "rainfall_mm",
        "temperature_c",
        "water_contamination_level",
    },
    "historical_alerts.csv": {"alert_id", "district_id", "alert_date", "alert_type", "severity", "status"},
}


def _resolve_csv_path(filename: str) -> Path:
    data_root = Path(settings.project_root, "backend", "data")
    exact = data_root / filename
    candidates: list[Path] = []
    if exact.exists():
        candidates.append(exact)
    if data_root.exists():
        candidates.extend(
            path for path in sorted(data_root.rglob(filename)) if path not in candidates
        )
    candidates.extend(
        path for path in sorted(Path(settings.project_root).glob(filename.replace(".csv", "*.csv"))) if path not in candidates
    )
    if not candidates:
        raise FileNotFoundError(f"Could not find required dataset file: {filename}")

    required_columns = REQUIRED_COLUMNS[filename]
    for candidate in candidates:
        with candidate.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            header = set(reader.fieldnames or [])
        if required_columns.issubset(header):
            return candidate

    return candidates[0]


def _csv_rows(filename: str) -> list[dict[str, str]]:
    path = _resolve_csv_path(filename)
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"{filename} is empty")

    missing = REQUIRED_COLUMNS[filename] - set(rows[0].keys())
    if missing:
        raise ValueError(f"{filename} is missing required columns: {sorted(missing)}")

    return rows


def _clear_database(db: Session) -> None:
    db.query(Alert).delete()
    db.query(Prediction).delete()
    db.query(DistrictDailyMetric).delete()
    db.query(Observation).delete()
    db.query(HistoricalAlert).delete()
    db.query(DistrictProfile).delete()
    db.query(District).delete()
    db.query(Setting).delete()
    db.commit()


def _normalize_severity(raw: str) -> str:
    value = (raw or "").strip().upper()
    if value in {"LOW", "MEDIUM", "HIGH"}:
        return value.lower()
    return "medium"


def _normalize_status(raw: str) -> str:
    value = (raw or "").strip().upper()
    if value in {"ACTIVE", "RESOLVED"}:
        return value.lower()
    return "resolved"


def reload_dataset(db: Session) -> dict[str, int]:
    _clear_database(db)

    master_rows = _csv_rows("district_master.csv")
    profile_rows = {row["district_id"].strip(): row for row in _csv_rows("district_profile.csv")}
    historical_rows = _csv_rows("historical_alerts.csv")
    observation_rows = _csv_rows("observations_base.csv")

    districts: dict[str, District] = {}
    for row in master_rows:
        district_id = row["district_id"].strip()
        profile = profile_rows.get(district_id)
        if profile is None:
            raise ValueError(f"district_profile.csv missing district_id {district_id}")

        district = District(
            district_id=district_id,
            district_name=row["district_name"].strip(),
            state=row["state"].strip(),
            population=int(float(row["population"])),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
        )
        district.profile = DistrictProfile(
            district_id=district_id,
            water_quality_index=float(profile["water_quality_index"]),
            sanitation_score=float(profile["sanitation_score"]),
            healthcare_access_score=float(profile["healthcare_access_score"]),
            population_density=float(profile["population_density"]),
            vulnerability_index=float(profile["vulnerability_index"]),
        )
        districts[district_id] = district
        db.add(district)
    db.flush()

    historical_dates_by_district: dict[str, list] = defaultdict(list)
    for row in historical_rows:
        district_id = row["district_id"].strip()
        if district_id not in districts:
            raise ValueError(f"historical_alerts.csv references unknown district_id {district_id}")

        alert_date = parse_date(row["alert_date"])
        historical_dates_by_district[district_id].append(alert_date)

        db.add(
            HistoricalAlert(
                external_alert_id=row["alert_id"].strip(),
                district_id=district_id,
                alert_date=alert_date,
                alert_type=row["alert_type"].strip(),
                severity=_normalize_severity(row["severity"]),
                status=_normalize_status(row["status"]),
            )
        )
    db.flush()

    aggregates: dict[tuple[str, object], dict[str, object]] = {}
    for row in observation_rows:
        district_id = row["district_id"].strip()
        if district_id not in districts:
            raise ValueError(f"observations_base.csv references unknown district_id {district_id}")

        observed_date = parse_date(row["date"])
        suspected_cases = int(float(row["suspected_cases"]))
        confirmed_cases = int(float(row["confirmed_cases"]))

        if suspected_cases < confirmed_cases:
            raise ValueError(
                f"Invalid observation {row['observation_id']}: suspected_cases < confirmed_cases"
            )

        observation = Observation(
            external_observation_id=row["observation_id"].strip(),
            district_id=district_id,
            zone=row["zone"].strip(),
            observed_date=observed_date,
            suspected_cases=suspected_cases,
            confirmed_cases=confirmed_cases,
            rainfall_mm=float(row["rainfall_mm"]),
            temperature_c=float(row["temperature_c"]),
            water_contamination_level=float(row["water_contamination_level"]),
        )
        db.add(observation)

        key = (district_id, observed_date)
        bucket = aggregates.setdefault(
            key,
            {
                "zones": set(),
                "suspected_cases": 0,
                "confirmed_cases": 0,
                "rainfall_values": [],
                "temperature_values": [],
                "contamination_values": [],
            },
        )
        bucket["zones"].add(row["zone"].strip())
        bucket["suspected_cases"] += suspected_cases
        bucket["confirmed_cases"] += confirmed_cases
        bucket["rainfall_values"].append(float(row["rainfall_mm"]))
        bucket["temperature_values"].append(float(row["temperature_c"]))
        bucket["contamination_values"].append(float(row["water_contamination_level"]))
    db.flush()

    metrics_by_district: dict[str, list[DistrictDailyMetric]] = defaultdict(list)
    for (district_id, observed_date), bucket in sorted(aggregates.items(), key=lambda item: (item[0][0], item[0][1])):
        metric = DistrictDailyMetric(
            district_id=district_id,
            observed_date=observed_date,
            zone_count=len(bucket["zones"]),
            total_suspected_cases=int(bucket["suspected_cases"]),
            total_confirmed_cases=int(bucket["confirmed_cases"]),
            avg_rainfall_mm=round(mean(bucket["rainfall_values"]), 3),
            avg_temperature_c=round(mean(bucket["temperature_values"]), 3),
            avg_water_contamination_level=round(mean(bucket["contamination_values"]), 3),
        )
        metrics_by_district[district_id].append(metric)
        db.add(metric)
    db.flush()

    prediction_count = 0
    for district_id, metric_series in metrics_by_district.items():
        if not metric_series:
            continue

        metric_series = sorted(metric_series, key=lambda metric: metric.observed_date)
        latest_metric = metric_series[-1]
        recent_window = metric_series[-7:]
        previous_window = metric_series[-14:-7]

        avg_confirmed_7d = mean(metric.total_confirmed_cases for metric in recent_window)
        avg_confirmed_prev_7d = mean(metric.total_confirmed_cases for metric in previous_window) if previous_window else avg_confirmed_7d
        avg_contamination_7d = mean(metric.avg_water_contamination_level for metric in recent_window)
        avg_rainfall_7d = mean(metric.avg_rainfall_mm for metric in recent_window)

        recent_alert_count = sum(
            1
            for alert_date in historical_dates_by_district[district_id]
            if 0 <= (latest_metric.observed_date - alert_date).days <= 30
        )

        profile = districts[district_id].profile
        result = compute_risk(
            RiskInputs(
                confirmed_cases_latest=latest_metric.total_confirmed_cases,
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

        db.add(
            Prediction(
                district_id=district_id,
                observed_date=latest_metric.observed_date,
                score=result.score,
                risk_level=result.risk_level,
                explanation=result.explanation,
                confirmed_cases_latest=latest_metric.total_confirmed_cases,
                avg_confirmed_cases_7d=round(avg_confirmed_7d, 2),
                avg_confirmed_cases_prev_7d=round(avg_confirmed_prev_7d, 2),
                contamination_7d=round(avg_contamination_7d, 3),
                rainfall_7d=round(avg_rainfall_7d, 3),
                vulnerability_index=profile.vulnerability_index,
                recent_alert_count=recent_alert_count,
            )
        )
        prediction_count += 1
    db.flush()

    db.add_all(
        [
            Setting(key="risk_low_threshold", value="0.4"),
            Setting(key="risk_high_threshold", value="0.7"),
            Setting(key="alerting_enabled", value="true"),
            Setting(key="auth_enabled", value=str(settings.auth_enabled).lower()),
            Setting(key="read_only_demo", value=str(settings.read_only_demo).lower()),
            Setting(key="district_count", value=str(len(master_rows))),
            Setting(key="historical_alert_rows", value=str(len(historical_rows))),
            Setting(key="observation_rows", value=str(len(observation_rows))),
            Setting(key="district_daily_metric_rows", value=str(len(aggregates))),
            Setting(key="prediction_rows", value=str(prediction_count)),
        ]
    )
    db.commit()
    regenerate_current_alerts(db)

    return {
        "districts": len(master_rows),
        "district_profiles": len(profile_rows),
        "historical_alerts": len(historical_rows),
        "observations": len(observation_rows),
        "district_daily_metrics": len(aggregates),
        "predictions": prediction_count,
    }


def bootstrap_database(db: Session) -> dict[str, int]:
    if db.query(District).count() > 0:
        return {
            "districts": db.query(District).count(),
            "district_profiles": db.query(DistrictProfile).count(),
            "historical_alerts": db.query(HistoricalAlert).count(),
            "observations": db.query(Observation).count(),
            "district_daily_metrics": db.query(DistrictDailyMetric).count(),
            "predictions": db.query(Prediction).count(),
        }

    return reload_dataset(db)
