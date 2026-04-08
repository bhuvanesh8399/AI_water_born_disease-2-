from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from app.db import Base


class District(Base):
    __tablename__ = "districts"

    district_id = Column(String, primary_key=True, index=True)
    district_name = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False, default="Tamil Nadu")
    population = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DistrictProfile(Base):
    __tablename__ = "district_profiles"

    district_id = Column(String, ForeignKey("districts.district_id"), primary_key=True)
    water_quality_index = Column(Float, nullable=True)
    sanitation_score = Column(Float, nullable=True)
    healthcare_access_score = Column(Float, nullable=True)
    population_density = Column(Float, nullable=True)
    vulnerability_index = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DistrictEnrichment(Base):
    __tablename__ = "district_enrichments"

    district_id = Column(String, ForeignKey("districts.district_id"), primary_key=True)
    district_name = Column(String, nullable=False)
    state_name = Column(String, nullable=False, default="Tamil Nadu")

    population_total = Column(Float, nullable=True)
    population_male = Column(Float, nullable=True)
    population_female = Column(Float, nullable=True)
    rural_population = Column(Float, nullable=True)
    urban_population = Column(Float, nullable=True)
    rural_population_pct = Column(Float, nullable=True)
    urban_population_pct = Column(Float, nullable=True)
    households_total = Column(Float, nullable=True)
    area_sq_km = Column(Float, nullable=True)
    population_density = Column(Float, nullable=True)
    literacy_rate_pct = Column(Float, nullable=True)

    sanitation_coverage_pct = Column(Float, nullable=True)
    households_with_latrine = Column(Float, nullable=True)
    households_without_latrine = Column(Float, nullable=True)
    households_open_defecation = Column(Float, nullable=True)

    drinking_water_coverage_pct = Column(Float, nullable=True)
    hh_treated_water_pct = Column(Float, nullable=True)
    piped_water_urban_pct = Column(Float, nullable=True)
    piped_water_rural_pct = Column(Float, nullable=True)
    water_quality_affected_pct = Column(Float, nullable=True)
    affected_habitations_total = Column(Float, nullable=True)
    primary_contaminant = Column(String, nullable=True)
    water_quality_risk_level = Column(String, nullable=True)
    water_samples_failed_pct = Column(Float, nullable=True)

    primary_health_centres = Column(Float, nullable=True)
    community_health_centres = Column(Float, nullable=True)
    total_health_facilities = Column(Float, nullable=True)
    estimated_hospital_beds = Column(Float, nullable=True)
    population_per_phc = Column(Float, nullable=True)

    vulnerability_score_raw = Column(Float, nullable=True)
    vulnerability_level = Column(String, nullable=True)
    poverty_rate_pct = Column(Float, nullable=True)
    avg_monthly_income_inr = Column(Float, nullable=True)
    waterborne_disease_index = Column(Float, nullable=True)
    public_health_risk_score = Column(Float, nullable=True)

    source_summary = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ObservationRaw(Base):
    __tablename__ = "observations_raw"

    id = Column(Integer, primary_key=True, index=True)
    source_observation_id = Column(Integer, nullable=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    observed_date = Column(Date, nullable=False, index=True)

    baseline_water_level = Column(Float, nullable=True)
    drainage_score = Column(Float, nullable=True)
    sanitation_score = Column(Float, nullable=True)
    population_density = Column(Float, nullable=True)
    vulnerability_index = Column(Float, nullable=True)
    anomaly_score = Column(Float, nullable=True)
    previous_alerts_count = Column(Integer, nullable=True)


class HistoricalAlert(Base):
    __tablename__ = "historical_alerts"

    alert_id = Column(String, primary_key=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    alert_date = Column(Date, nullable=False, index=True)
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False)


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=True)
    temperature_max_c = Column(Float, nullable=True)
    temperature_min_c = Column(Float, nullable=True)
    source = Column(String, nullable=False, default="open-meteo")

    __table_args__ = (
        UniqueConstraint("district_id", "date", "source", name="uq_weather_district_date_source"),
    )


class DistrictDailyMetric(Base):
    __tablename__ = "district_daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    observed_date = Column(Date, nullable=False, index=True)

    avg_baseline_water_level = Column(Float, nullable=True)
    avg_drainage_score = Column(Float, nullable=True)
    sanitation_score = Column(Float, nullable=True)
    population_density = Column(Float, nullable=True)
    vulnerability_index = Column(Float, nullable=True)
    anomaly_score = Column(Float, nullable=True)
    previous_alerts_count = Column(Integer, nullable=True)
    historical_alert_count = Column(Integer, nullable=True, default=0)

    __table_args__ = (
        UniqueConstraint("district_id", "observed_date", name="uq_metric_district_date"),
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    predicted_date = Column(Date, nullable=False, index=True)

    rule_score = Column(Float, nullable=True)
    rf_score = Column(Float, nullable=True)
    xgb_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)

    data_completeness = Column(Float, nullable=True)
    data_freshness_score = Column(Float, nullable=True)
    model_agreement_score = Column(Float, nullable=True)

    reasons_json = Column(Text, nullable=True)
    recommended_actions_json = Column(Text, nullable=True)
    chosen_model = Column(String, nullable=False, default="HYBRID")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("district_id", "predicted_date", name="uq_prediction_district_date"),
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String, ForeignKey("districts.district_id"), nullable=False, index=True)
    predicted_date = Column(Date, nullable=False, index=True)

    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)
    owner_role = Column(String, nullable=False, default="District Health Officer")
    reasons_json = Column(Text, nullable=True)
    recommended_actions_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "district_id",
            "predicted_date",
            "severity",
            name="uq_alert_district_date_severity",
        ),
    )
