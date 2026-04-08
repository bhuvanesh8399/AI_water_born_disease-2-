import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.models import Alert, District, Observation, RiskPrediction, Setting, User
from app.services.alert_engine import maybe_create_alerts
from app.services.risk_engine import compute_risk_prediction


def seed_database(db: Session) -> None:
    if db.query(User).first():
        return

    settings = get_settings()

    admin = User(
        email=settings.default_admin_email,
        full_name="System Admin",
        role="admin",
        password_hash=hash_password(settings.default_admin_password),
    )
    analyst = User(
        email=settings.default_analyst_email,
        full_name="Field Analyst",
        role="analyst",
        password_hash=hash_password(settings.default_analyst_password),
    )
    db.add_all([admin, analyst])

    districts = [
        District(code="D001", name="Chennai", latitude=13.0827, longitude=80.2707),
        District(code="D002", name="Madurai", latitude=9.9252, longitude=78.1198),
        District(code="D003", name="Coimbatore", latitude=11.0168, longitude=76.9558),
        District(code="D004", name="Salem", latitude=11.6643, longitude=78.1460),
    ]
    db.add_all(districts)
    db.flush()

    today = date.today()
    rng = random.Random(42)

    for district in districts:
        latest_prediction = None
        for offset in range(14, 0, -1):
            observed_on = today - timedelta(days=offset)
            obs = Observation(
                district_id=district.id,
                observed_on=observed_on,
                rainfall_mm=round(rng.uniform(5, 130), 2),
                water_level=round(rng.uniform(20, 95), 2),
                fever_cases=rng.randint(4, 42),
                contamination_index=round(rng.uniform(0.1, 0.95), 2),
                source="seed",
            )
            db.add(obs)
            db.flush()
            latest_prediction = compute_risk_prediction(db, district.id, observed_on)

        if latest_prediction:
            maybe_create_alerts(db, district.id, latest_prediction)

    db.add_all(
        [
            Setting(key="data_mode", value="api"),
            Setting(key="refresh_interval_seconds", value="60"),
            Setting(key="alert_threshold", value="65"),
            Setting(key="default_district", value="D001"),
        ]
    )

    db.commit()
