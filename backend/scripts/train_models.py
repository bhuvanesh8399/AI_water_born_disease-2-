import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.db import SessionLocal
from app.services.pipeline_service import load_artifacts, train_models


if __name__ == "__main__":
    db = SessionLocal()
    try:
        result = train_models(db)
        load_artifacts()
        print(result)
    finally:
        db.close()
