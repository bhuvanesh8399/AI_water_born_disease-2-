from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sqlalchemy import func
from sqlalchemy.orm import Session

try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None

from app.config import DATA_DIR, META_PATH, RF_PATH, XGB_PATH
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

FILE_ALIASES = {
    "villupuram": "viluppuram",
    "tirupattur": "tirupathur",
    "tirupathur": "tirupathur",
    "thoothukkudi": "thoothukudi",
    "the nilgiris": "nilgiris",
}

FEATURE_COLUMNS = [
    "avg_baseline_water_level",
    "avg_drainage_score",
    "sanitation_score",
    "metric_population_density",
    "metric_vulnerability_index",
    "anomaly_score",
    "previous_alerts_count",
    "historical_alert_count",
    "profile_water_quality_index",
    "profile_sanitation_score",
    "profile_healthcare_access_score",
    "profile_population_density",
    "profile_vulnerability_index",
    "enrich_population_total",
    "enrich_population_density",
    "enrich_rural_population_pct",
    "enrich_urban_population_pct",
    "enrich_literacy_rate_pct",
    "enrich_sanitation_coverage_pct",
    "enrich_drinking_water_coverage_pct",
    "enrich_water_quality_affected_pct",
    "enrich_primary_health_centres",
    "enrich_total_health_facilities",
    "enrich_estimated_hospital_beds",
    "enrich_population_per_phc",
    "enrich_vulnerability_score_raw",
    "enrich_waterborne_disease_index",
    "enrich_public_health_risk_score",
    "enrich_poverty_rate_pct",
]

MODEL_CACHE: Dict[str, Any] = {
    "rf": None,
    "xgb": None,
    "meta": {"features": [], "fill_values": {}},
}


def now_utc() -> datetime:
    return datetime.utcnow()


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def resolve_column(df: pd.DataFrame, *candidates: str, required: bool = True) -> Optional[str]:
    header_map = {normalize_header(col): col for col in df.columns}
    for candidate in candidates:
        key = normalize_header(candidate)
        if key in header_map:
            return header_map[key]
    if required:
        raise KeyError(f"Missing required column. Tried {candidates}. Available: {list(df.columns)}")
    return None


def rename_resolved(
    df: pd.DataFrame,
    required_map: Dict[str, List[str]],
    optional_map: Optional[Dict[str, List[str]]] = None,
) -> pd.DataFrame:
    rename_map: Dict[str, str] = {}
    for target, candidates in required_map.items():
        rename_map[resolve_column(df, *candidates, required=True)] = target
    for target, candidates in (optional_map or {}).items():
        found = resolve_column(df, *candidates, required=False)
        if found:
            rename_map[found] = target
    return df.rename(columns=rename_map)


def find_file(*needles: str) -> Path:
    all_csvs = list(DATA_DIR.rglob("*.csv"))
    for file in all_csvs:
        lower = file.name.lower()
        if all(needle.lower() in lower for needle in needles):
            return file
    raise FileNotFoundError(f"Could not find CSV matching: {needles} in {DATA_DIR}")


def read_csv_safe(*needles: str) -> pd.DataFrame:
    path = find_file(*needles)
    return pd.read_csv(path)


def read_csv_optional(*needles: str) -> pd.DataFrame:
    try:
        return read_csv_safe(*needles)
    except FileNotFoundError:
        return pd.DataFrame()


def parse_date(value: Any) -> Optional[date]:
    if value is None or pd.isna(value):
        return None
    return pd.to_datetime(value).date()


def as_float(value: Any) -> Optional[float]:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except Exception:
        return None


def as_int(value: Any) -> Optional[int]:
    if value is None or pd.isna(value):
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def normalize_name(value: Any) -> str:
    s = str(value).strip().lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    return FILE_ALIASES.get(s, s)


def normalize_district_id(value: Any) -> Optional[str]:
    if value is None or pd.isna(value):
        return None
    s = str(value).strip().upper()
    if s.startswith("D") and s[1:].isdigit():
        return f"D{int(s[1:]):03d}"
    if s.isdigit():
        return f"D{int(s):03d}"
    match = re.search(r"(\d+)", s)
    if match:
        return f"D{int(match.group(1)):03d}"
    return None


def coalesce(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, float) and np.isnan(value):
            continue
        return value
    return None


def risk_level_from_score(score: float) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def json_dumps_safe(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def json_loads_safe(value: Optional[str]) -> Any:
    if not value:
        return []
    try:
        return json.loads(value)
    except Exception:
        return []


def chunked(rows: List[dict], size: int = 5000):
    for i in range(0, len(rows), size):
        yield rows[i : i + size]


def load_artifacts() -> None:
    MODEL_CACHE["rf"] = joblib.load(RF_PATH) if RF_PATH.exists() else None
    MODEL_CACHE["xgb"] = joblib.load(XGB_PATH) if XGB_PATH.exists() else None
    MODEL_CACHE["meta"] = (
        joblib.load(META_PATH) if META_PATH.exists() else {"features": FEATURE_COLUMNS, "fill_values": {}}
    )


def clear_core_tables(db: Session) -> None:
    db.query(Alert).delete()
    db.query(Prediction).delete()
    db.query(DistrictDailyMetric).delete()
    db.query(ObservationRaw).delete()
    db.query(HistoricalAlert).delete()
    db.query(WeatherObservation).delete()
    db.query(DistrictEnrichment).delete()
    db.query(DistrictProfile).delete()
    db.query(District).delete()
    db.commit()


def ingest_core_data(db: Session) -> dict:
    master_df = rename_resolved(
        read_csv_safe("district_master"),
        required_map={
            "district_id": ["district_id", "district code"],
            "district_name": ["district_name", "district"],
        },
        optional_map={
            "state": ["state", "state_name"],
            "population": ["population", "population_total"],
            "latitude": ["latitude", "lat"],
            "longitude": ["longitude", "lon", "lng"],
        },
    )
    profile_df = rename_resolved(
        read_csv_safe("district_profile"),
        required_map={"district_id": ["district_id", "district code"]},
        optional_map={
            "water_quality_index": ["water_quality_index"],
            "sanitation_score": ["sanitation_score"],
            "healthcare_access_score": ["healthcare_access_score"],
            "population_density": ["population_density"],
            "vulnerability_index": ["vulnerability_index"],
        },
    )
    obs_df = rename_resolved(
        read_csv_safe("observations_base"),
        required_map={
            "district_id": ["district_id", "district code"],
            "observed_date": ["observed_date", "date"],
        },
        optional_map={
            "source_observation_id": ["observation_id", "id"],
            "baseline_water_level": ["baseline_water_level"],
            "drainage_score": ["drainage_score"],
            "sanitation_score": ["sanitation_score"],
            "population_density": ["population_density"],
            "vulnerability_index": ["vulnerability_index"],
            "anomaly_score": ["anomaly_score"],
            "previous_alerts_count": ["previous_alerts_count"],
        },
    )
    hist_df = rename_resolved(
        read_csv_safe("historical_alerts"),
        required_map={
            "alert_id": ["alert_id", "id"],
            "district_id": ["district_id", "district code"],
            "alert_date": ["alert_date", "date"],
            "alert_type": ["alert_type", "type"],
            "severity": ["severity"],
        },
        optional_map={"status": ["status"]},
    )

    master_df["district_id"] = master_df["district_id"].map(normalize_district_id)
    profile_df["district_id"] = profile_df["district_id"].map(normalize_district_id)
    obs_df["district_id"] = obs_df["district_id"].map(normalize_district_id)
    hist_df["district_id"] = hist_df["district_id"].map(normalize_district_id)

    clear_core_tables(db)

    district_rows = []
    for _, row in master_df.iterrows():
        if not row.get("district_id") or not row.get("district_name"):
            continue
        district_rows.append(
            {
                "district_id": row["district_id"],
                "district_name": str(row["district_name"]).strip(),
                "state": str(coalesce(row.get("state"), "Tamil Nadu")).strip(),
                "population": as_float(row.get("population")),
                "latitude": as_float(row.get("latitude")),
                "longitude": as_float(row.get("longitude")),
            }
        )
    if district_rows:
        db.bulk_insert_mappings(District, district_rows)
    db.commit()

    valid_districts = {row["district_id"] for row in district_rows}

    profile_rows = []
    for _, row in profile_df.iterrows():
        district_id = row.get("district_id")
        if district_id not in valid_districts:
            continue
        profile_rows.append(
            {
                "district_id": district_id,
                "water_quality_index": as_float(row.get("water_quality_index")),
                "sanitation_score": as_float(row.get("sanitation_score")),
                "healthcare_access_score": as_float(row.get("healthcare_access_score")),
                "population_density": as_float(row.get("population_density")),
                "vulnerability_index": as_float(row.get("vulnerability_index")),
            }
        )
    if profile_rows:
        db.bulk_insert_mappings(DistrictProfile, profile_rows)
    db.commit()

    hist_rows = []
    for _, row in hist_df.iterrows():
        district_id = row.get("district_id")
        if district_id not in valid_districts:
            continue
        hist_rows.append(
            {
                "alert_id": str(row["alert_id"]),
                "district_id": district_id,
                "alert_date": parse_date(row["alert_date"]),
                "alert_type": str(row["alert_type"]),
                "severity": str(row["severity"]).upper(),
                "status": str(coalesce(row.get("status"), "CLOSED")).upper(),
            }
        )
    if hist_rows:
        db.bulk_insert_mappings(HistoricalAlert, hist_rows)
    db.commit()

    obs_rows = []
    obs_df = obs_df[obs_df["district_id"].isin(valid_districts)].copy()
    for _, row in obs_df.iterrows():
        observed_date = parse_date(row.get("observed_date"))
        if not observed_date:
            continue
        obs_rows.append(
            {
                "source_observation_id": as_int(row.get("source_observation_id")),
                "district_id": row["district_id"],
                "observed_date": observed_date,
                "baseline_water_level": as_float(row.get("baseline_water_level")),
                "drainage_score": as_float(row.get("drainage_score")),
                "sanitation_score": as_float(row.get("sanitation_score")),
                "population_density": as_float(row.get("population_density")),
                "vulnerability_index": as_float(row.get("vulnerability_index")),
                "anomaly_score": as_float(row.get("anomaly_score")),
                "previous_alerts_count": as_int(row.get("previous_alerts_count")),
            }
        )
    for chunk in chunked(obs_rows, 5000):
        db.bulk_insert_mappings(ObservationRaw, chunk)
        db.commit()

    metric_count = aggregate_daily_metrics(db)

    return {
        "districts_loaded": len(district_rows),
        "profiles_loaded": len(profile_rows),
        "historical_alerts_loaded": len(hist_rows),
        "observations_loaded": len(obs_rows),
        "district_daily_metrics_loaded": metric_count,
    }


def aggregate_daily_metrics(db: Session) -> int:
    obs_df = pd.read_sql(
        db.query(
            ObservationRaw.district_id,
            ObservationRaw.observed_date,
            ObservationRaw.baseline_water_level,
            ObservationRaw.drainage_score,
            ObservationRaw.sanitation_score,
            ObservationRaw.population_density,
            ObservationRaw.vulnerability_index,
            ObservationRaw.anomaly_score,
            ObservationRaw.previous_alerts_count,
        ).statement,
        db.bind,
    )
    if obs_df.empty:
        db.query(DistrictDailyMetric).delete()
        db.commit()
        return 0

    obs_df["observed_date"] = pd.to_datetime(obs_df["observed_date"])
    grouped = (
        obs_df.groupby(["district_id", "observed_date"], as_index=False)
        .agg(
            avg_baseline_water_level=("baseline_water_level", "mean"),
            avg_drainage_score=("drainage_score", "mean"),
            sanitation_score=("sanitation_score", "mean"),
            population_density=("population_density", "mean"),
            vulnerability_index=("vulnerability_index", "mean"),
            anomaly_score=("anomaly_score", "mean"),
            previous_alerts_count=("previous_alerts_count", "max"),
        )
    )

    hist_df = pd.read_sql(
        db.query(HistoricalAlert.district_id, HistoricalAlert.alert_date).statement,
        db.bind,
    )
    if not hist_df.empty:
        hist_df["alert_date"] = pd.to_datetime(hist_df["alert_date"])
        hist_counts = (
            hist_df.groupby(["district_id", "alert_date"], as_index=False)
            .size()
            .rename(columns={"size": "historical_alert_count"})
        )
        grouped = grouped.merge(
            hist_counts,
            left_on=["district_id", "observed_date"],
            right_on=["district_id", "alert_date"],
            how="left",
        )
        grouped["historical_alert_count"] = grouped["historical_alert_count"].fillna(0)
    else:
        grouped["historical_alert_count"] = 0

    rows = []
    for _, row in grouped.iterrows():
        rows.append(
            {
                "district_id": row["district_id"],
                "observed_date": row["observed_date"].date(),
                "avg_baseline_water_level": as_float(row.get("avg_baseline_water_level")),
                "avg_drainage_score": as_float(row.get("avg_drainage_score")),
                "sanitation_score": as_float(row.get("sanitation_score")),
                "population_density": as_float(row.get("population_density")),
                "vulnerability_index": as_float(row.get("vulnerability_index")),
                "anomaly_score": as_float(row.get("anomaly_score")),
                "previous_alerts_count": as_int(row.get("previous_alerts_count")) or 0,
                "historical_alert_count": as_int(row.get("historical_alert_count")) or 0,
            }
        )

    db.query(DistrictDailyMetric).delete()
    db.commit()
    for chunk in chunked(rows, 5000):
        db.bulk_insert_mappings(DistrictDailyMetric, chunk)
        db.commit()
    return len(rows)


def latest_prefixed(df: pd.DataFrame, prefix: str, state_filter: bool = True) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["norm_name"])

    df = rename_resolved(
        df,
        required_map={"district_name": ["district_name", "district"]},
        optional_map={"state_name": ["state_name", "state"], "year": ["year", "source_year"]},
    ).copy()
    if state_filter and "state_name" in df.columns:
        df = df[df["state_name"].astype(str).str.lower().eq("tamil nadu")]

    df["norm_name"] = df["district_name"].map(normalize_name)

    if "year" in df.columns:
        df = df.sort_values("year").groupby("norm_name", as_index=False).tail(1)
    else:
        df = df.drop_duplicates(subset=["norm_name"], keep="last")

    keep_cols = ["norm_name"]
    for col in df.columns:
        if col in {"norm_name", "district_name", "state_name"}:
            continue
        keep_cols.append(col)

    df = df[keep_cols].copy()
    rename_map = {"norm_name": "norm_name"}
    for col in df.columns:
        if col == "norm_name":
            continue
        rename_map[col] = f"{prefix}_{col}"
    return df.rename(columns=rename_map)


def ingest_enrichment_data(db: Session) -> dict:
    master_df = rename_resolved(
        read_csv_safe("district_master"),
        required_map={
            "district_id": ["district_id", "district code"],
            "district_name": ["district_name", "district"],
        },
        optional_map={"state": ["state", "state_name"]},
    )
    base = master_df[["district_id", "district_name"]].copy()
    base["state"] = master_df["state"] if "state" in master_df.columns else "Tamil Nadu"
    base["district_id"] = base["district_id"].map(normalize_district_id)
    base["norm_name"] = base["district_name"].map(normalize_name)

    tn_df = latest_prefixed(read_csv_optional("tamil_nadu_district_health_water_risk"), "tn", state_filter=False)
    pop_df = latest_prefixed(read_csv_optional("population_district_india"), "pop")
    rural_df = latest_prefixed(read_csv_optional("rural_urban_population_district_india"), "rural")
    san_df = latest_prefixed(read_csv_optional("sanitation_district_india"), "san")
    dw_df = latest_prefixed(read_csv_optional("drinking_water_access_district_india"), "dw")
    wq_df = latest_prefixed(read_csv_optional("water_quality_district_india"), "wq")
    hi_df = latest_prefixed(read_csv_optional("health_infrastructure_district_india"), "hi")
    vuln_df = latest_prefixed(read_csv_optional("district_vulnerability_india"), "vuln")

    merged = base.copy()
    for frame in [tn_df, pop_df, rural_df, san_df, dw_df, wq_df, hi_df, vuln_df]:
        merged = merged.merge(frame, on="norm_name", how="left")

    db.query(DistrictEnrichment).delete()
    db.commit()

    rows = []
    for _, row in merged.iterrows():
        sources = []
        for source_prefix in ["tn_", "pop_", "rural_", "san_", "dw_", "wq_", "hi_", "vuln_"]:
            if any(not pd.isna(row.get(col)) for col in merged.columns if col.startswith(source_prefix)):
                sources.append(source_prefix[:-1])

        rows.append(
            {
                "district_id": normalize_district_id(row["district_id"]),
                "district_name": str(row["district_name"]),
                "state_name": str(coalesce(row.get("state"), "Tamil Nadu")),
                "population_total": as_float(coalesce(row.get("tn_population_total"), row.get("pop_population_total"))),
                "population_male": as_float(coalesce(row.get("tn_population_male"), row.get("pop_population_male"))),
                "population_female": as_float(coalesce(row.get("tn_population_female"), row.get("pop_population_female"))),
                "rural_population": as_float(coalesce(row.get("tn_rural_population"), row.get("rural_rural_population"))),
                "urban_population": as_float(coalesce(row.get("tn_urban_population"), row.get("rural_urban_population"))),
                "rural_population_pct": as_float(coalesce(row.get("tn_rural_population_pct"), row.get("rural_rural_population_pct"))),
                "urban_population_pct": as_float(coalesce(row.get("tn_urban_population_pct"), row.get("rural_urban_population_pct"))),
                "households_total": as_float(coalesce(row.get("tn_households_total"), row.get("pop_households_total"), row.get("san_households_total"))),
                "area_sq_km": as_float(coalesce(row.get("tn_area_sq_km"), row.get("pop_area_sq_km"))),
                "population_density": as_float(coalesce(row.get("tn_population_density"), row.get("pop_population_density"), row.get("vuln_population_density"))),
                "literacy_rate_pct": as_float(coalesce(row.get("tn_literacy_rate_pct"), row.get("pop_literacy_rate_pct"), row.get("vuln_literacy_rate_pct"))),
                "sanitation_coverage_pct": as_float(coalesce(row.get("tn_sanitation_coverage_pct"), row.get("san_sanitation_coverage_pct"), row.get("vuln_sanitation_coverage_pct"))),
                "households_with_latrine": as_float(coalesce(row.get("tn_hh_with_latrine"), row.get("san_households_with_latrine"))),
                "households_without_latrine": as_float(coalesce(row.get("tn_hh_without_latrine"), row.get("san_households_without_latrine"))),
                "households_open_defecation": as_float(coalesce(row.get("san_households_open_defecation"))),
                "drinking_water_coverage_pct": as_float(coalesce(row.get("tn_drinking_water_coverage_pct"), row.get("dw_drinking_water_coverage_pct"), row.get("vuln_drinking_water_coverage_pct"))),
                "hh_treated_water_pct": as_float(coalesce(row.get("tn_hh_treated_water_pct"), row.get("dw_households_treated_water_pct"))),
                "piped_water_urban_pct": as_float(coalesce(row.get("tn_piped_water_urban_pct"), row.get("dw_piped_water_urban_pct"))),
                "piped_water_rural_pct": as_float(coalesce(row.get("tn_piped_water_rural_pct"), row.get("dw_piped_water_rural_pct"))),
                "water_quality_affected_pct": as_float(coalesce(row.get("vuln_water_quality_affected_pct"), row.get("wq_affected_pct"))),
                "affected_habitations_total": as_float(coalesce(row.get("wq_affected_habitations_total"), row.get("tn_total_wq_affected_habitations"))),
                "primary_contaminant": coalesce(row.get("wq_primary_contaminant")),
                "water_quality_risk_level": coalesce(row.get("wq_water_quality_risk_level")),
                "water_samples_failed_pct": as_float(coalesce(row.get("tn_water_samples_failed_pct"))),
                "primary_health_centres": as_float(coalesce(row.get("tn_phc_count"), row.get("hi_primary_health_centres"), row.get("vuln_primary_health_centres"))),
                "community_health_centres": as_float(coalesce(row.get("tn_chc_count"), row.get("hi_community_health_centres"))),
                "total_health_facilities": as_float(coalesce(row.get("tn_total_govt_health_facilities"), row.get("hi_total_health_facilities"))),
                "estimated_hospital_beds": as_float(coalesce(row.get("tn_govt_hospital_beds"), row.get("hi_estimated_hospital_beds"))),
                "population_per_phc": as_float(coalesce(row.get("hi_population_per_phc"), row.get("vuln_population_per_phc"))),
                "vulnerability_score_raw": as_float(coalesce(row.get("tn_vulnerability_score_raw"), row.get("vuln_vulnerability_score_raw"))),
                "vulnerability_level": coalesce(row.get("vuln_vulnerability_level"), row.get("tn_risk_tier")),
                "poverty_rate_pct": as_float(coalesce(row.get("tn_poverty_rate_pct"))),
                "avg_monthly_income_inr": as_float(coalesce(row.get("tn_avg_monthly_income_inr"))),
                "waterborne_disease_index": as_float(coalesce(row.get("tn_waterborne_disease_index"))),
                "public_health_risk_score": as_float(coalesce(row.get("tn_public_health_risk_score"))),
                "source_summary": json_dumps_safe(sources),
            }
        )

    if rows:
        db.bulk_insert_mappings(DistrictEnrichment, rows)
    db.commit()
    return {"district_enrichments_loaded": len(rows)}


async def fetch_weather_payload(latitude: float, longitude: float) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 7,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        return response.json()


async def ingest_weather(db: Session) -> dict:
    districts = db.query(District).all()
    rows_processed = 0
    for district in districts:
        if district.latitude is None or district.longitude is None:
            continue

        payload = await fetch_weather_payload(district.latitude, district.longitude)
        daily = payload.get("daily", {})
        days = daily.get("time", [])
        rainfall = daily.get("precipitation_sum", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])

        for i, day_str in enumerate(days):
            day = parse_date(day_str)
            if not day:
                continue

            existing = (
                db.query(WeatherObservation)
                .filter(
                    WeatherObservation.district_id == district.district_id,
                    WeatherObservation.date == day,
                    WeatherObservation.source == "open-meteo",
                )
                .first()
            )

            values = {
                "district_id": district.district_id,
                "date": day,
                "latitude": district.latitude,
                "longitude": district.longitude,
                "rainfall_mm": as_float(rainfall[i]) if i < len(rainfall) else None,
                "temperature_max_c": as_float(tmax[i]) if i < len(tmax) else None,
                "temperature_min_c": as_float(tmin[i]) if i < len(tmin) else None,
                "source": "open-meteo",
            }

            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
            else:
                db.add(WeatherObservation(**values))
            rows_processed += 1

        db.commit()

    return {"weather_rows_processed": rows_processed}


def build_training_frame(db: Session) -> pd.DataFrame:
    query = (
        db.query(
            DistrictDailyMetric.district_id.label("district_id"),
            DistrictDailyMetric.observed_date.label("observed_date"),
            DistrictDailyMetric.avg_baseline_water_level.label("avg_baseline_water_level"),
            DistrictDailyMetric.avg_drainage_score.label("avg_drainage_score"),
            DistrictDailyMetric.sanitation_score.label("sanitation_score"),
            DistrictDailyMetric.population_density.label("metric_population_density"),
            DistrictDailyMetric.vulnerability_index.label("metric_vulnerability_index"),
            DistrictDailyMetric.anomaly_score.label("anomaly_score"),
            DistrictDailyMetric.previous_alerts_count.label("previous_alerts_count"),
            DistrictDailyMetric.historical_alert_count.label("historical_alert_count"),
            DistrictProfile.water_quality_index.label("profile_water_quality_index"),
            DistrictProfile.sanitation_score.label("profile_sanitation_score"),
            DistrictProfile.healthcare_access_score.label("profile_healthcare_access_score"),
            DistrictProfile.population_density.label("profile_population_density"),
            DistrictProfile.vulnerability_index.label("profile_vulnerability_index"),
            DistrictEnrichment.population_total.label("enrich_population_total"),
            DistrictEnrichment.population_density.label("enrich_population_density"),
            DistrictEnrichment.rural_population_pct.label("enrich_rural_population_pct"),
            DistrictEnrichment.urban_population_pct.label("enrich_urban_population_pct"),
            DistrictEnrichment.literacy_rate_pct.label("enrich_literacy_rate_pct"),
            DistrictEnrichment.sanitation_coverage_pct.label("enrich_sanitation_coverage_pct"),
            DistrictEnrichment.drinking_water_coverage_pct.label("enrich_drinking_water_coverage_pct"),
            DistrictEnrichment.water_quality_affected_pct.label("enrich_water_quality_affected_pct"),
            DistrictEnrichment.primary_health_centres.label("enrich_primary_health_centres"),
            DistrictEnrichment.total_health_facilities.label("enrich_total_health_facilities"),
            DistrictEnrichment.estimated_hospital_beds.label("enrich_estimated_hospital_beds"),
            DistrictEnrichment.population_per_phc.label("enrich_population_per_phc"),
            DistrictEnrichment.vulnerability_score_raw.label("enrich_vulnerability_score_raw"),
            DistrictEnrichment.waterborne_disease_index.label("enrich_waterborne_disease_index"),
            DistrictEnrichment.public_health_risk_score.label("enrich_public_health_risk_score"),
            DistrictEnrichment.poverty_rate_pct.label("enrich_poverty_rate_pct"),
        )
        .outerjoin(DistrictProfile, DistrictProfile.district_id == DistrictDailyMetric.district_id)
        .outerjoin(DistrictEnrichment, DistrictEnrichment.district_id == DistrictDailyMetric.district_id)
    )

    df = pd.read_sql(query.statement, db.bind)
    if df.empty:
        return df

    df["observed_date"] = pd.to_datetime(df["observed_date"]).dt.date
    hist_df = pd.read_sql(
        db.query(HistoricalAlert.district_id, HistoricalAlert.alert_date, HistoricalAlert.severity).statement,
        db.bind,
    )

    positive_dates = defaultdict(set)
    if not hist_df.empty:
        hist_df["alert_date"] = pd.to_datetime(hist_df["alert_date"]).dt.date
        hist_df["severity"] = hist_df["severity"].astype(str).str.upper()
        hist_df = hist_df[hist_df["severity"].isin(["HIGH", "MEDIUM"])]
        for _, row in hist_df.iterrows():
            for offset in range(0, 8):
                positive_dates[row["district_id"]].add(row["alert_date"] - timedelta(days=offset))

    df["target"] = df.apply(
        lambda row: 1 if row["observed_date"] in positive_dates[row["district_id"]] else 0,
        axis=1,
    )
    return df


def train_models(db: Session) -> dict:
    df = build_training_frame(db)
    if df.empty:
        raise ValueError("No training data available")
    if df["target"].nunique() < 2:
        raise ValueError("Training target has only one class. Check historical alerts.")

    df = df.sort_values("observed_date").reset_index(drop=True)
    unique_dates = sorted(df["observed_date"].unique())
    cutoff_index = max(int(len(unique_dates) * 0.8), 1)
    cutoff_date = unique_dates[cutoff_index - 1]

    train_df = df[df["observed_date"] <= cutoff_date].copy()
    val_df = df[df["observed_date"] > cutoff_date].copy()
    if val_df.empty:
        val_df = train_df.tail(min(2000, len(train_df))).copy()

    X_train = train_df[FEATURE_COLUMNS].copy()
    y_train = train_df["target"].astype(int)
    X_val = val_df[FEATURE_COLUMNS].copy()
    y_val = val_df["target"].astype(int)

    imputer = SimpleImputer(strategy="median")
    X_train_imp = imputer.fit_transform(X_train)
    X_val_imp = imputer.transform(X_val)

    rf = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=4,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train_imp, y_train)
    rf_pred = rf.predict(X_val_imp)
    rf_prob = rf.predict_proba(X_val_imp)[:, 1]

    rf_metrics = {
        "accuracy": round(float(accuracy_score(y_val, rf_pred)), 4),
        "precision": round(float(precision_score(y_val, rf_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_val, rf_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_val, rf_pred, zero_division=0)), 4),
        "avg_positive_probability": round(float(np.mean(rf_prob)), 4),
    }

    xgb = None
    xgb_metrics = None
    if XGBClassifier is not None:
        xgb = XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            reg_lambda=1.0,
            random_state=42,
            eval_metric="logloss",
        )
        xgb.fit(X_train_imp, y_train)
        xgb_pred = xgb.predict(X_val_imp)
        xgb_prob = xgb.predict_proba(X_val_imp)[:, 1]
        xgb_metrics = {
            "accuracy": round(float(accuracy_score(y_val, xgb_pred)), 4),
            "precision": round(float(precision_score(y_val, xgb_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_val, xgb_pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_val, xgb_pred, zero_division=0)), 4),
            "avg_positive_probability": round(float(np.mean(xgb_prob)), 4),
        }

    fill_values = {}
    for feature in FEATURE_COLUMNS:
        series = X_train[feature].replace([np.inf, -np.inf], np.nan)
        fill_values[feature] = float(series.median()) if not series.dropna().empty else 0.0

    joblib.dump(rf, RF_PATH)
    if xgb is not None:
        joblib.dump(xgb, XGB_PATH)
    joblib.dump(
        {
            "features": FEATURE_COLUMNS,
            "fill_values": fill_values,
            "trained_at": datetime.utcnow().isoformat(),
            "cutoff_date": str(cutoff_date),
        },
        META_PATH,
    )
    load_artifacts()

    return {
        "rows_total": len(df),
        "rows_train": len(train_df),
        "rows_val": len(val_df),
        "rf_metrics": rf_metrics,
        "xgb_metrics": xgb_metrics,
        "xgb_available": XGBClassifier is not None,
    }


def get_latest_metric(db: Session, district_id: str) -> Optional[DistrictDailyMetric]:
    return (
        db.query(DistrictDailyMetric)
        .filter(DistrictDailyMetric.district_id == district_id)
        .order_by(DistrictDailyMetric.observed_date.desc())
        .first()
    )


def get_latest_weather(db: Session, district_id: str) -> Optional[WeatherObservation]:
    return (
        db.query(WeatherObservation)
        .filter(WeatherObservation.district_id == district_id)
        .order_by(WeatherObservation.date.desc())
        .first()
    )


def get_recent_alerts_count(db: Session, district_id: str, days: int = 30) -> int:
    since = date.today() - timedelta(days=days)
    return (
        db.query(func.count(HistoricalAlert.alert_id))
        .filter(
            HistoricalAlert.district_id == district_id,
            HistoricalAlert.alert_date >= since,
        )
        .scalar()
        or 0
    )


def calculate_rule_score(
    metric: Optional[DistrictDailyMetric],
    profile: Optional[DistrictProfile],
    enrich: Optional[DistrictEnrichment],
    weather: Optional[WeatherObservation],
    recent_alerts_count: int,
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    rainfall = weather.rainfall_mm if weather else None
    if rainfall is not None:
        if rainfall >= 50:
            score += 14
            reasons.append("Heavy rainfall signal in latest weather feed")
        elif rainfall >= 20:
            score += 8
            reasons.append("Moderate rainfall signal in latest weather feed")

    anomaly = metric.anomaly_score if metric else None
    if anomaly is not None:
        if anomaly >= 0.7:
            score += 14
            reasons.append("High anomaly score in district observations")
        elif anomaly >= 0.4:
            score += 7
            reasons.append("Moderate anomaly score in district observations")

    drainage = metric.avg_drainage_score if metric else None
    if drainage is not None:
        if drainage < 40:
            score += 10
            reasons.append("Low drainage score increases stagnation risk")
        elif drainage < 60:
            score += 5
            reasons.append("Moderate drainage weakness present")

    sanitation = coalesce(
        profile.sanitation_score if profile else None,
        metric.sanitation_score if metric else None,
        enrich.sanitation_coverage_pct if enrich else None,
    )
    if sanitation is not None:
        if sanitation < 40:
            score += 12
            reasons.append("Poor sanitation conditions detected")
        elif sanitation < 60:
            score += 6
            reasons.append("Sanitation coverage is not strong enough")

    wq_index = profile.water_quality_index if profile else None
    if wq_index is not None and wq_index < 50:
        score += 10
        reasons.append("Water quality index is weak")

    water_quality_affected = enrich.water_quality_affected_pct if enrich else None
    if water_quality_affected is not None:
        if water_quality_affected >= 10:
            score += 12
            reasons.append("Large share of habitations affected by water quality issues")
        elif water_quality_affected >= 5:
            score += 6
            reasons.append("Water quality issues present in the district")

    vulnerability = coalesce(
        profile.vulnerability_index if profile else None,
        enrich.vulnerability_score_raw if enrich else None,
        metric.vulnerability_index if metric else None,
    )
    if vulnerability is not None:
        if vulnerability >= 70:
            score += 12
            reasons.append("District vulnerability is high")
        elif vulnerability >= 50:
            score += 6
            reasons.append("District vulnerability is moderately elevated")

    density = coalesce(
        enrich.population_density if enrich else None,
        profile.population_density if profile else None,
        metric.population_density if metric else None,
    )
    if density is not None:
        if density >= 1500:
            score += 8
            reasons.append("High population density may accelerate spread")
        elif density >= 700:
            score += 4
            reasons.append("Moderate population density pressure detected")

    healthcare_access = profile.healthcare_access_score if profile else None
    population_per_phc = enrich.population_per_phc if enrich else None
    if healthcare_access is not None and healthcare_access < 40:
        score += 8
        reasons.append("Healthcare access score is weak")
    if population_per_phc is not None and population_per_phc > 50000:
        score += 6
        reasons.append("Primary healthcare load is high")

    previous_alerts = metric.previous_alerts_count if metric else 0
    if previous_alerts and previous_alerts >= 3:
        score += 8
        reasons.append("Repeated previous alerts suggest persistent district pressure")
    elif recent_alerts_count >= 2:
        score += 6
        reasons.append("Recent historical alerts reinforce ongoing risk")

    return round(min(score, 100.0), 2), reasons


def build_feature_row(
    metric: Optional[DistrictDailyMetric],
    profile: Optional[DistrictProfile],
    enrich: Optional[DistrictEnrichment],
) -> dict:
    return {
        "avg_baseline_water_level": metric.avg_baseline_water_level if metric else None,
        "avg_drainage_score": metric.avg_drainage_score if metric else None,
        "sanitation_score": metric.sanitation_score if metric else None,
        "metric_population_density": metric.population_density if metric else None,
        "metric_vulnerability_index": metric.vulnerability_index if metric else None,
        "anomaly_score": metric.anomaly_score if metric else None,
        "previous_alerts_count": metric.previous_alerts_count if metric else 0,
        "historical_alert_count": metric.historical_alert_count if metric else 0,
        "profile_water_quality_index": profile.water_quality_index if profile else None,
        "profile_sanitation_score": profile.sanitation_score if profile else None,
        "profile_healthcare_access_score": profile.healthcare_access_score if profile else None,
        "profile_population_density": profile.population_density if profile else None,
        "profile_vulnerability_index": profile.vulnerability_index if profile else None,
        "enrich_population_total": enrich.population_total if enrich else None,
        "enrich_population_density": enrich.population_density if enrich else None,
        "enrich_rural_population_pct": enrich.rural_population_pct if enrich else None,
        "enrich_urban_population_pct": enrich.urban_population_pct if enrich else None,
        "enrich_literacy_rate_pct": enrich.literacy_rate_pct if enrich else None,
        "enrich_sanitation_coverage_pct": enrich.sanitation_coverage_pct if enrich else None,
        "enrich_drinking_water_coverage_pct": enrich.drinking_water_coverage_pct if enrich else None,
        "enrich_water_quality_affected_pct": enrich.water_quality_affected_pct if enrich else None,
        "enrich_primary_health_centres": enrich.primary_health_centres if enrich else None,
        "enrich_total_health_facilities": enrich.total_health_facilities if enrich else None,
        "enrich_estimated_hospital_beds": enrich.estimated_hospital_beds if enrich else None,
        "enrich_population_per_phc": enrich.population_per_phc if enrich else None,
        "enrich_vulnerability_score_raw": enrich.vulnerability_score_raw if enrich else None,
        "enrich_waterborne_disease_index": enrich.waterborne_disease_index if enrich else None,
        "enrich_public_health_risk_score": enrich.public_health_risk_score if enrich else None,
        "enrich_poverty_rate_pct": enrich.poverty_rate_pct if enrich else None,
    }


def predict_ml_score(model_key: str, feature_row: dict) -> Optional[float]:
    model = MODEL_CACHE.get(model_key)
    meta = MODEL_CACHE.get("meta") or {"features": FEATURE_COLUMNS, "fill_values": {}}
    features = meta.get("features") or FEATURE_COLUMNS
    fill_values = meta.get("fill_values") or {}

    if model is None:
        return None

    row = []
    for feature in features:
        value = feature_row.get(feature)
        if value is None or (isinstance(value, float) and np.isnan(value)):
            value = fill_values.get(feature, 0.0)
        row.append(float(value))

    probability = float(model.predict_proba([row])[0][1])
    return round(probability * 100.0, 2)


def level_agreement_score(*scores: Optional[float]) -> float:
    present_scores = [s for s in scores if s is not None]
    if not present_scores:
        return 0.4
    levels = [risk_level_from_score(s) for s in present_scores]
    unique = set(levels)
    if len(unique) == 1:
        return 1.0
    if len(unique) == 2:
        return 0.72
    return 0.45


def freshness_score(metric: Optional[DistrictDailyMetric], weather: Optional[WeatherObservation]) -> float:
    today = date.today()

    metric_score = 0.3
    if metric:
        age = (today - metric.observed_date).days
        if age <= 7:
            metric_score = 1.0
        elif age <= 30:
            metric_score = 0.75
        elif age <= 90:
            metric_score = 0.55

    weather_score = 0.3
    if weather:
        age = abs((today - weather.date).days)
        if age <= 2:
            weather_score = 1.0
        elif age <= 7:
            weather_score = 0.7
        else:
            weather_score = 0.45

    return round((metric_score + weather_score) / 2.0, 2)


def completeness_score(feature_row: dict, weather: Optional[WeatherObservation]) -> float:
    values = list(feature_row.values())
    if weather is not None:
        values.extend([weather.rainfall_mm, weather.temperature_max_c, weather.temperature_min_c])
    total = len(values)
    present = sum(
        1
        for value in values
        if value is not None and not (isinstance(value, float) and np.isnan(value))
    )
    return round(present / total, 2) if total else 0.0


def recommended_actions_from_risk(risk_level: str, reasons: list[str]) -> list[str]:
    actions: list[str] = []
    if risk_level == "HIGH":
        actions.extend(
            [
                "Notify District Health Officer immediately",
                "Dispatch field inspection teams to water and sanitation hotspots",
                "Alert public hospitals and primary health centres for surge readiness",
                "Increase water quality testing and chlorination monitoring",
                "Issue local preventive advisory for affected communities",
            ]
        )
    elif risk_level == "MEDIUM":
        actions.extend(
            [
                "Increase district surveillance and local monitoring",
                "Review sanitation and drinking water weak points",
                "Prepare PHCs and district control room for escalation",
            ]
        )
    else:
        actions.extend(
            [
                "Continue routine monitoring",
                "Watch for rainfall and anomaly changes",
            ]
        )

    lowered_reasons = " ".join(reasons).lower()
    if "water quality" in lowered_reasons:
        actions.append("Prioritize water source testing and contamination tracing")
    if "sanitation" in lowered_reasons:
        actions.append("Review sanitation coverage and hygiene enforcement in vulnerable clusters")
    if "rainfall" in lowered_reasons:
        actions.append("Inspect flood-prone drainage channels and stagnant water locations")

    deduped = []
    seen = set()
    for action in actions:
        if action not in seen:
            seen.add(action)
            deduped.append(action)
    return deduped


def generate_predictions(db: Session) -> dict:
    load_artifacts()
    today = date.today()

    db.query(Alert).filter(Alert.predicted_date == today).delete()
    db.query(Prediction).filter(Prediction.predicted_date == today).delete()
    db.commit()

    districts = db.query(District).all()
    predictions_created = 0
    alerts_created = 0

    for district in districts:
        metric = get_latest_metric(db, district.district_id)
        profile = db.query(DistrictProfile).filter(DistrictProfile.district_id == district.district_id).first()
        enrich = db.query(DistrictEnrichment).filter(DistrictEnrichment.district_id == district.district_id).first()
        weather = get_latest_weather(db, district.district_id)
        recent_hist_count = get_recent_alerts_count(db, district.district_id)

        rule_score, reasons = calculate_rule_score(metric, profile, enrich, weather, recent_hist_count)
        feature_row = build_feature_row(metric, profile, enrich)
        rf_score = predict_ml_score("rf", feature_row)
        xgb_score = predict_ml_score("xgb", feature_row)

        weighted_scores = []
        weights = []

        weighted_scores.append(rule_score * 0.45)
        weights.append(0.45)

        if rf_score is not None:
            weighted_scores.append(rf_score * 0.25)
            weights.append(0.25)
        if xgb_score is not None:
            weighted_scores.append(xgb_score * 0.30)
            weights.append(0.30)

        final_score = round(sum(weighted_scores) / sum(weights), 2) if weights else rule_score

        agreement = level_agreement_score(rule_score, rf_score, xgb_score)
        freshness = freshness_score(metric, weather)
        completeness = completeness_score(feature_row, weather)
        confidence = round((completeness * 0.4 + freshness * 0.3 + agreement * 0.3) * 100.0, 2)

        if rf_score is not None and rf_score >= 70:
            reasons.append("Random Forest reinforced elevated district risk")
        if xgb_score is not None and xgb_score >= 70:
            reasons.append("XGBoost reinforced elevated district risk")
        if not reasons:
            reasons = ["Baseline indicators remain stable; continue monitoring"]

        risk_level = risk_level_from_score(final_score)
        actions = recommended_actions_from_risk(risk_level, reasons)

        db.add(
            Prediction(
                district_id=district.district_id,
                predicted_date=today,
                rule_score=rule_score,
                rf_score=rf_score,
                xgb_score=xgb_score,
                final_score=final_score,
                risk_level=risk_level,
                confidence_score=confidence,
                data_completeness=round(completeness * 100.0, 2),
                data_freshness_score=round(freshness * 100.0, 2),
                model_agreement_score=round(agreement * 100.0, 2),
                reasons_json=json_dumps_safe(reasons[:8]),
                recommended_actions_json=json_dumps_safe(actions),
                chosen_model="HYBRID_RULE_RF_XGB",
            )
        )
        predictions_created += 1

        if risk_level in {"HIGH", "MEDIUM"}:
            db.add(
                Alert(
                    district_id=district.district_id,
                    predicted_date=today,
                    severity=risk_level,
                    status="ACTIVE",
                    title=f"{risk_level} risk detected for {district.district_name}",
                    message=f"{district.district_name} flagged with {risk_level} risk. Review reasons and recommended actions immediately.",
                    confidence_score=confidence,
                    owner_role="District Health Officer",
                    reasons_json=json_dumps_safe(reasons[:8]),
                    recommended_actions_json=json_dumps_safe(actions),
                )
            )
            alerts_created += 1

    db.commit()
    return {
        "predictions_created": predictions_created,
        "alerts_created": alerts_created,
    }


def ensure_today_predictions(db: Session) -> None:
    count = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.predicted_date == date.today())
        .scalar()
        or 0
    )
    if count == 0:
        generate_predictions(db)


async def run_full_pipeline(db: Session) -> dict:
    core = ingest_core_data(db)
    enrichment = ingest_enrichment_data(db)
    weather = await ingest_weather(db)
    try:
        training = train_models(db)
    except Exception as exc:
        training = {"warning": str(exc)}
    predictions = generate_predictions(db)
    return {
        "core": core,
        "enrichment": enrichment,
        "weather": weather,
        "training": training,
        "predictions": predictions,
    }
