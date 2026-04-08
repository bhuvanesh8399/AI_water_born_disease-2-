from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class District(Base):
    __tablename__ = "districts"

    district_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    district_name: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str] = mapped_column(String(120))
    population: Mapped[int] = mapped_column(Integer, default=0)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    profile = relationship(
        "DistrictProfile",
        back_populates="district",
        uselist=False,
        cascade="all, delete-orphan",
    )
    observations = relationship("Observation", back_populates="district", cascade="all, delete-orphan")
    daily_metrics = relationship("DistrictDailyMetric", back_populates="district", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="district", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="district", cascade="all, delete-orphan")
    historical_alerts = relationship("HistoricalAlert", back_populates="district", cascade="all, delete-orphan")


class DistrictProfile(Base):
    __tablename__ = "district_profiles"

    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), primary_key=True)
    water_quality_index: Mapped[float] = mapped_column(Float, default=0)
    sanitation_score: Mapped[float] = mapped_column(Float, default=0)
    healthcare_access_score: Mapped[float] = mapped_column(Float, default=0)
    population_density: Mapped[float] = mapped_column(Float, default=0)
    vulnerability_index: Mapped[float] = mapped_column(Float, default=0)

    district = relationship("District", back_populates="profile")


class HistoricalAlert(Base):
    __tablename__ = "historical_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_alert_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), index=True)
    alert_date: Mapped[date] = mapped_column(Date, index=True)
    alert_type: Mapped[str] = mapped_column(String(80))
    severity: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(20), index=True)

    district = relationship("District", back_populates="historical_alerts")


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_observation_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), index=True)
    zone: Mapped[str] = mapped_column(String(32), index=True)
    observed_date: Mapped[date] = mapped_column(Date, index=True)
    suspected_cases: Mapped[int] = mapped_column(Integer, default=0)
    confirmed_cases: Mapped[int] = mapped_column(Integer, default=0)
    rainfall_mm: Mapped[float] = mapped_column(Float, default=0)
    temperature_c: Mapped[float] = mapped_column(Float, default=0)
    water_contamination_level: Mapped[float] = mapped_column(Float, default=0)

    district = relationship("District", back_populates="observations")


class DistrictDailyMetric(Base):
    __tablename__ = "district_daily_metrics"
    __table_args__ = (UniqueConstraint("district_id", "observed_date", name="uq_metric_district_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), index=True)
    observed_date: Mapped[date] = mapped_column(Date, index=True)
    zone_count: Mapped[int] = mapped_column(Integer, default=0)
    total_suspected_cases: Mapped[int] = mapped_column(Integer, default=0)
    total_confirmed_cases: Mapped[int] = mapped_column(Integer, default=0)
    avg_rainfall_mm: Mapped[float] = mapped_column(Float, default=0)
    avg_temperature_c: Mapped[float] = mapped_column(Float, default=0)
    avg_water_contamination_level: Mapped[float] = mapped_column(Float, default=0)

    district = relationship("District", back_populates="daily_metrics")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), index=True)
    observed_date: Mapped[date] = mapped_column(Date, index=True)
    score: Mapped[float] = mapped_column(Float, index=True)
    risk_level: Mapped[str] = mapped_column(String(20), index=True)
    explanation: Mapped[str] = mapped_column(Text)

    confirmed_cases_latest: Mapped[int] = mapped_column(Integer, default=0)
    avg_confirmed_cases_7d: Mapped[float] = mapped_column(Float, default=0)
    avg_confirmed_cases_prev_7d: Mapped[float] = mapped_column(Float, default=0)
    contamination_7d: Mapped[float] = mapped_column(Float, default=0)
    rainfall_7d: Mapped[float] = mapped_column(Float, default=0)
    vulnerability_index: Mapped[float] = mapped_column(Float, default=0)
    recent_alert_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    district = relationship("District", back_populates="predictions")
    alerts = relationship("Alert", back_populates="prediction")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.district_id"), index=True)
    prediction_id: Mapped[int | None] = mapped_column(ForeignKey("predictions.id"), nullable=True, index=True)
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    title: Mapped[str] = mapped_column(String(180))
    message: Mapped[str] = mapped_column(Text)
    score: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    district = relationship("District", back_populates="alerts")
    prediction = relationship("Prediction", back_populates="alerts")


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    value: Mapped[str] = mapped_column(String(255))
