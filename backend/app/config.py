import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ews.db")
DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data"))).resolve()
MODEL_ARTIFACT_DIR = Path(
    os.getenv("MODEL_ARTIFACT_DIR", str(BASE_DIR / "artifacts"))
).resolve()

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

RF_PATH = MODEL_ARTIFACT_DIR / "rf.joblib"
XGB_PATH = MODEL_ARTIFACT_DIR / "xgb.joblib"
META_PATH = MODEL_ARTIFACT_DIR / "model_meta.joblib"

FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
